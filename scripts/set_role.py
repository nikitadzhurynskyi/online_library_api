import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select
from src.db.database import session_maker
from src.user.model import User, UserRole


async def change_user_role():
    print("Changing user role script loaded.")
    email = input("Write a user email: ").strip()

    available_roles = [r.name for r in UserRole]
    print(f"Available roles: {', '.join(available_roles)}")

    role_input = input("Write a new role for user: ").strip().upper()

    try:
        new_role = UserRole[role_input]
    except KeyError:
        print(f"❌ ERROR: Role '{role_input}' does not exist!")
        return

    async with session_maker() as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ User with email - '{email}' not in database!")
            return

        if user.role == new_role:
            print(f"ℹ️ User with email - {email} has role - {new_role.value}")
            return

        old_role = user.role.value
        user.role = new_role

        await session.commit()

        print(f"✅ Role for user with {email} changed: {old_role} -> {new_role.value}")


if __name__ == "__main__":
    asyncio.run(change_user_role())