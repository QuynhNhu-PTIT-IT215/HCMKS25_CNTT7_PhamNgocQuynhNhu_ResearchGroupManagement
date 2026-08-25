from datetime import datetime, timezone, timedelta

from app.db.database import SessionLocal, Base, engine

from app.models.user import User
from app.models.research_project import ResearchProject, ResearchMember
from app.models.research_task import ResearchTask

from app.core.security import get_password_hash


def seed_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        users = [
            User(
                email="nguyenvana@gmail.com",
                password_hash=get_password_hash("123456"),
                full_name="Nguyễn Văn An",
                role="User",
                is_active=True
            ),
            User(
                email="tranthibinh@gmail.com",
                password_hash=get_password_hash("123456"),
                full_name="Trần Thị Bình",
                role="User",
                is_active=True
            ),
            User(
                email="levancuong@gmail.com",
                password_hash=get_password_hash("123456"),
                full_name="Lê Văn Cường",
                role="User",
                is_active=True
            ),
            User(
                email="phamthilan@gmail.com",
                password_hash=get_password_hash("123456"),
                full_name="Phạm Thị Lan",
                role="User",
                is_active=True
            ),
            User(
                email="admin@gmail.com",
                password_hash=get_password_hash("123456"),
                full_name="Admin",
                role="Admin",
                is_active=True
            )
        ]

        for user in users:
            db.add(user)

        db.commit()

        for user in users:
            db.refresh(user)

        user1 = users[0]
        user2 = users[1]
        user3 = users[2]
        user4 = users[3]

        project1 = ResearchProject(
            name="Ứng dụng AI trong giáo dục",
            description="Nghiên cứu ứng dụng trí tuệ nhân tạo vào việc hỗ trợ giảng dạy và học tập.",
            owner_id=user1.id
        )

        project2 = ResearchProject(
            name="Hệ thống quản lý nghiên cứu khoa học",
            description="Xây dựng hệ thống quản lý đề tài, thành viên và nhiệm vụ nghiên cứu.",
            owner_id=user2.id
        )

        project3 = ResearchProject(
            name="Phân tích dữ liệu sinh viên",
            description="Nghiên cứu phương pháp phân tích dữ liệu nhằm hỗ trợ quản lý sinh viên.",
            owner_id=user3.id
        )

        db.add_all([
            project1,
            project2,
            project3
        ])

        db.commit()

        db.refresh(project1)
        db.refresh(project2)
        db.refresh(project3)

        members = [
            ResearchMember(
                project_id=project1.id,
                user_id=user1.id,
                role="Owner"
            ),
            ResearchMember(
                project_id=project1.id,
                user_id=user2.id,
                role="Member"
            ),
            ResearchMember(
                project_id=project1.id,
                user_id=user3.id,
                role="Member"
            ),
            ResearchMember(
                project_id=project2.id,
                user_id=user2.id,
                role="Owner"
            ),
            ResearchMember(
                project_id=project2.id,
                user_id=user1.id,
                role="Member"
            ),
            ResearchMember(
                project_id=project2.id,
                user_id=user4.id,
                role="Member"
            ),
            ResearchMember(
                project_id=project3.id,
                user_id=user3.id,
                role="Owner"
            ),
            ResearchMember(
                project_id=project3.id,
                user_id=user4.id,
                role="Member"
            )
        ]

        db.add_all(members)

        db.commit()

        now = datetime.now(timezone.utc)

        tasks = [
            ResearchTask(
                project_id=project1.id,
                title="Khảo sát nhu cầu người học",
                description="Khảo sát nhu cầu sử dụng AI của sinh viên.",
                assignee_id=user2.id,
                status="TODO",
                priority="HIGH",
                due_date=now + timedelta(days=7)
            ),
            ResearchTask(
                project_id=project1.id,
                title="Xây dựng mô hình AI",
                description="Nghiên cứu và xây dựng mô hình AI thử nghiệm.",
                assignee_id=user3.id,
                status="IN_PROGRESS",
                priority="MEDIUM",
                due_date=now + timedelta(days=14)
            ),
            ResearchTask(
                project_id=project2.id,
                title="Thiết kế cơ sở dữ liệu",
                description="Thiết kế database cho hệ thống quản lý nghiên cứu.",
                assignee_id=user1.id,
                status="DONE",
                priority="HIGH",
                due_date=now - timedelta(days=2)
            ),
            ResearchTask(
                project_id=project2.id,
                title="Xây dựng API",
                description="Xây dựng các API quản lý đề tài nghiên cứu.",
                assignee_id=user4.id,
                status="IN_PROGRESS",
                priority="HIGH",
                due_date=now + timedelta(days=10)
            ),
            ResearchTask(
                project_id=project3.id,
                title="Thu thập dữ liệu sinh viên",
                description="Thu thập dữ liệu phục vụ nghiên cứu.",
                assignee_id=user4.id,
                status="TODO",
                priority="MEDIUM",
                due_date=now + timedelta(days=5)
            ),
            ResearchTask(
                project_id=project3.id,
                title="Phân tích dữ liệu",
                description="Phân tích dữ liệu và đưa ra kết quả nghiên cứu.",
                assignee_id=user3.id,
                status="IN_PROGRESS",
                priority="LOW",
                due_date=now + timedelta(days=20)
            )
        ]

        db.add_all(tasks)

        db.commit()

        print("Seed dữ liệu thành công!")

        print("Users: 5")
        print("Research Projects: 3")
        print("Research Members: 8")
        print("Research Tasks: 6")

    except Exception as e:
        db.rollback()
        print("Seed dữ liệu thất bại:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()