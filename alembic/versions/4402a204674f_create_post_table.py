"""Create post table

Revision ID: 4402a204674f
Revises: 
Create Date: 2025-01-14 21:31:08.297525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4402a204674f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
