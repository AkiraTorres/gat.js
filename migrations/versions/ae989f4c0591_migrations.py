"""migrations

Revision ID: ae989f4c0591
Revises: 
Create Date: 2023-12-04 17:18:20.734511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae989f4c0591'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aluno', schema=None) as batch_op:
        batch_op.alter_column('ano_entrada',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['cpf'])

    with op.batch_alter_table('disciplina', schema=None) as batch_op:
        batch_op.alter_column('codigo',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('disciplina', schema=None) as batch_op:
        batch_op.alter_column('codigo',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=8),
               existing_nullable=False)

    with op.batch_alter_table('aluno', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('ano_entrada',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
