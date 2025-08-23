"""Change is_transcript_ready from Boolean to String

Revision ID: d088e70d011a
Revises: 2ba58d239dab
Create Date: 2025-08-19 00:20:49.158781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd088e70d011a'
down_revision: Union[str, Sequence[str], None] = '2ba58d239dab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем старую колонку
    op.drop_column('audio_files', 'is_transcript_ready')

    # Добавляем новую колонку с типом String
    op.add_column('audio_files', sa.Column('is_transcript_ready', sa.String(), nullable=True))


    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('audio_files', 'is_transcript_ready')
    op.add_column('audio_files', sa.Column('is_transcript_ready', sa.Boolean(), nullable=True))


