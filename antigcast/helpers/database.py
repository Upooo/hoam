import datetime
from typing import List, Optional
from pytz import timezone
from antigcast.config import MONGO_DB_URI, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client[DB_NAME]

userdb = db['USERS']
actchat = db['ACTIVEDVEDCHATS']
blackword = db['BLACKWORDS']
owner = db['OWNERS']
exp = db['EXP']
globaldb = db['GLOBALMUTE']
mutedb = db['GROUPMUTE']
sellers_collection = db['ADDSELLER']
sellerr_collection = db['SELLERINFO']
state = db['STATEDB']
superankes_state = db['SPRSTATEDB']
approved = db['APPROVEDUSER']

#USERS
def new_user(id):
    return dict(
        id=id,
        join_date=datetime.date.today().isoformat(),
        ban_status=dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        ),
    )


async def add_user(id):
    user = new_user(id)
    await userdb.insert_one(user)


async def is_user_exist(id):
    user = await userdb.find_one({"id": int(id)})
    return bool(user)


async def total_users_count():
    count = await userdb.count_documents({})
    return count


async def get_all_users():
    return userdb.find({})


async def delete_user(user_id):
    await userdb.delete_many({"id": int(user_id)})


async def remove_ban(id):
    ban_status = dict(
        is_banned=False,
        ban_duration=0,
        banned_on=datetime.date.max.isoformat(),
        ban_reason="",
    )
    await userdb.update_one({"id": id}, {"$set": {"ban_status": ban_status}})


async def ban_user(user_id, ban_duration, ban_reason):
    ban_status = dict(
        is_banned=True,
        ban_duration=ban_duration,
        banned_on=datetime.date.today().isoformat(),
        ban_reason=ban_reason,
    )
    await userdb.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})


async def get_ban_status(id):
    default = dict(
        is_banned=False,
        ban_duration=0,
        banned_on=datetime.date.max.isoformat(),
        ban_reason="",
    )
    user = await userdb.find_one({"id": int(id)})
    return user.get("ban_status", default)


async def get_all_banned_users():
    return userdb.find({"ban_status.is_banned": True})
    

# ACTIVED_CHATS
async def get_actived_chats() -> list:
    acctivedchats = await actchat.find_one({"acctivedchat": "acctivedchat"})
    if not acctivedchats:
        return []
    return acctivedchats["acctivedchats"]


async def add_actived_chat(trigger) -> bool:
    acctivedchats = await get_actived_chats()
    acctivedchats.append(trigger)
    await actchat.update_one({"acctivedchat": "acctivedchat"}, {"$set": {"acctivedchats": acctivedchats}}, upsert=True)
    return True


async def rem_actived_chat(trigger) -> bool:
    acctivedchats = await get_actived_chats()
    if trigger in acctivedchats:
        acctivedchats.remove(trigger)
        await actchat.update_one({"acctivedchat": "acctivedchat"}, {"$set": {"acctivedchats": acctivedchats}}, upsert=True)
        return True
    else:
        return False

async def get_state(chat_id: int) -> Optional[bool]:
    state_info = await state.find_one({"chat_id": chat_id})
    return state_info.get("state") if state_info else None

async def set_state(chat_id: int, state_val: bool) -> bool:
    if not isinstance(state_val, bool):
        raise ValueError("State harus boolean (True/False)")
    result = await state.update_one({"chat_id": chat_id}, {"$set": {"state": state_val}}, upsert=True)
    return result.upserted_id is not None or result.modified_count > 0

async def get_superankes_state(chat_id: int) -> Optional[bool]:
    state_info = await superankes_state.find_one({"chat_id": chat_id})
    return state_info.get("superankes_state") if state_info else None

async def set_superankes_state(chat_id: int, state_val: bool) -> bool:
    if not isinstance(state_val, bool):
        raise ValueError("State harus boolean (True/False)")
    result = await superankes_state.update_one({"chat_id": chat_id}, {"$set": {"superankes_state": state_val}}, upsert=True)
    return result.upserted_id is not None or result.modified_count > 0

async def count_groups() -> int:
    return await state.count_documents({})

async def get_all_chat_ids() -> List[int]:
    cursor = state.find({})
    return [doc["chat_id"] async for doc in cursor]

async def add_free_user(chat_id: int, user_id: int) -> bool:
    try:
        await approved.insert_one({"chat_id": chat_id, "user_id": user_id})
        return True
    except Exception:
        return False

async def delete_free_user(chat_id: int, user_id: int) -> bool:
    try:
        result = await approved.delete_one({"chat_id": chat_id, "user_id": user_id})
        return result.deleted_count == 1
    except Exception:
        return False

async def get_free_user(chat_id: int) -> List[dict]:
    try:
        cursor = approved.find({"chat_id": chat_id})
        return [doc async for doc in cursor]
    except Exception:
        return []

async def is_free_user(chat_id: int, user_id: int) -> bool:
    try:
        user = await approved.find_one({"chat_id": chat_id, "user_id": user_id})
        return user is not None
    except Exception:
        return False
    
# BLACKLIST_WORD
async def get_bl_words() -> list:
    filters = await blackword.find_one({"filter": "filter"})
    if not filters:
        return []
    return filters["filters"]

async def add_bl_word(trigger) -> bool:
    x = trigger.lower()
    filters = await get_bl_words()
    filters.append(x)
    await blackword.update_one({"filter": "filter"}, {"$set": {"filters": filters}}, upsert=True)
    return True

async def remove_bl_word(trigger) -> bool:
    x = trigger.lower()
    filters = await get_bl_words()
    filters.remove(x)
    await blackword.update_one({"filter": "filter"}, {"$set": {"filters": filters}}, upsert=True)
    return True

# OWNER
async def get_owners() -> list:
    owners = await owner.find_one({"owner": "owner"})
    if not owners:
        return []
    return owners["owners"]


async def add_owner(trigger) -> bool:
    owners = await get_owners()
    owners.append(trigger)
    await owner.update_one({"owner": "owner"}, {"$set": {"owners": owners}}, upsert=True)
    return True


async def remove_owner(trigger) -> bool:
    owners = await get_owners()
    owners.remove(trigger)
    await owner.update_one({"owner": "owner"}, {"$set": {"owners": owners}}, upsert=True)
    return True
    


# GLOBAL_DELETE
async def get_muted_users() -> list:
    mutedusers = await globaldb.find_one({"muteduser": "muteduser"})
    if not mutedusers:
        return []
    return mutedusers["mutedusers"]


async def mute_user(uid_id) -> bool:
    mutedusers = await get_muted_users()
    mutedusers.append(uid_id)
    await globaldb.update_one({"muteduser": "muteduser"}, {"$set": {"mutedusers": mutedusers}}, upsert=True)
    return True


async def unmute_user(uid_id) -> bool:
    mutedusers = await get_muted_users()
    mutedusers.remove(uid_id)
    await globaldb.update_one({"muteduser": "muteduser"}, {"$set": {"mutedusers": mutedusers}}, upsert=True)
    return True

# GROUP_MUTE
async def mute_user_in_group(group_id, user_id, muted_by_id, muted_by_name):
    await mutedb.update_one(
        {'group_id': group_id},
        {'$addToSet': {'muted_users': {'user_id': user_id, 'muted_by': {'id': muted_by_id, 'name': muted_by_name}}}},
        upsert=True
    )

async def unmute_user_in_group(group_id, user_id):
    await mutedb.update_one(
        {'group_id': group_id},
        {'$pull': {'muted_users': {'user_id': user_id}}}
    )

async def get_muted_users_in_group(group_id):
    doc = await mutedb.find_one({'group_id': group_id})
    if doc:
        return doc.get('muted_users', [])
    return []

async def clear_muted_users_in_group(group_id):
    await mutedb.delete_one({'group_id': group_id})
    