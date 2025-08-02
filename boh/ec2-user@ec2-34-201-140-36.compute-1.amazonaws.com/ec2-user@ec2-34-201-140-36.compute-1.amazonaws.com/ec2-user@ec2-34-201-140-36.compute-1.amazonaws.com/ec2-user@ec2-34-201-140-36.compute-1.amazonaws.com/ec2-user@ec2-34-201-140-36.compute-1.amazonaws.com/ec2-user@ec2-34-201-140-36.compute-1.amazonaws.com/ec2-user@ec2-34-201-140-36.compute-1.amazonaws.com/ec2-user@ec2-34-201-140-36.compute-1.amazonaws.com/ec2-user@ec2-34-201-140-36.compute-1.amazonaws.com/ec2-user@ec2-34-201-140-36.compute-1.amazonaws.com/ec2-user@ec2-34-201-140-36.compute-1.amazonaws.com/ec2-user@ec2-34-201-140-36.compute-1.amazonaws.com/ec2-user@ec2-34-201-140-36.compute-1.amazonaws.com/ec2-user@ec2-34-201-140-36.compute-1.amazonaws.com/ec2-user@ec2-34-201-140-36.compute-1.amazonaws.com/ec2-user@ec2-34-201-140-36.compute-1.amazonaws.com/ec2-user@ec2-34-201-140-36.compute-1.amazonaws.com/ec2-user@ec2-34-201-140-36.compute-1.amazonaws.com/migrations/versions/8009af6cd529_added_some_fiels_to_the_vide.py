"""added some fields to the videos

Revision ID: 8009af6cd529
Revises: b920029ed617
Create Date: 2024-10-01 16:57:51.176945

"""
from alembic import op
import sqlalchemy as sa
import uuid  # Import the uuid module for generating unique values

# revision identifiers, used by Alembic.
revision = '8009af6cd529'
down_revision = 'b920029ed617'
branch_labels = None
depends_on = None


def upgrade():
    # ### Step 1: Add columns as nullable ###
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ref', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('public_url', sa.String(length=255), nullable=True))

    # ### Step 2: Populate existing rows with unique values ###
    connection = op.get_bind()

    # Option 1: Using PostgreSQL's uuid_generate_v4()
    connection.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
    connection.execute(sa.text("""
        UPDATE videos
        SET
            ref = uuid_generate_v4(),
            public_url = 'https://yourdomain.com/videos/' || uuid_generate_v4()
        WHERE ref IS NULL OR public_url IS NULL;
    """))

    # Option 2: Using Python's uuid module (Uncomment if you prefer this method)
    # videos_to_update = connection.execute(sa.text("SELECT id FROM videos WHERE ref IS NULL OR public_url IS NULL")).fetchall()
    # for video in videos_to_update:
    #     unique_ref = str(uuid.uuid4())
    #     unique_public_url = f"https://yourdomain.com/videos/{uuid.uuid4()}"
    #     connection.execute(
    #         sa.text("UPDATE videos SET ref = :ref, public_url = :public_url WHERE id = :id"),
    #         {"ref": unique_ref, "public_url": unique_public_url, "id": video.id}
    #     )

    # ### Step 3: Alter columns to be non-nullable ###
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.alter_column(
            'ref',
            existing_type=sa.String(length=255),
            nullable=False
        )
        batch_op.alter_column(
            'public_url',
            existing_type=sa.String(length=255),
            nullable=False
        )

    # ### Step 4: Add unique constraints with explicit names ###
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_videos_ref', ['ref'])
        batch_op.create_unique_constraint('uq_videos_public_url', ['public_url'])


def downgrade():
    # ### Commands to reverse the upgrade ###
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_constraint('uq_videos_public_url', type_='unique')
        batch_op.drop_constraint('uq_videos_ref', type_='unique')
        batch_op.drop_column('public_url')
        batch_op.drop_column('ref')
    # ### end Alembic commands ###
