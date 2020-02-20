"""create cow table

Revision ID: 04658d0dab42
Revises: 
Create Date: 2020-02-18 22:05:18.342280

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "04658d0dab42"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cow",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pregnant", sa.Boolean(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("cow")
