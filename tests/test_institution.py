import pytest

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, select

from src.models.institution import Institution


def test_create_institution(db_session):
    institution = Institution(
        name="UBS Teste",
        institution_type="ubs",
    )

    db_session.add(institution)
    db_session.commit()
    db_session.refresh(institution)

    assert institution.id is not None
    assert institution.name == "UBS Teste"
    assert institution.institution_type == "ubs"


def test_institution_default_values(db_session):
    institution = Institution(
        name="UBS Teste 2",
        institution_type="ubs",
    )

    db_session.add(institution)
    db_session.commit()
    db_session.refresh(institution)

    assert institution.is_local_stock_owner is False
    assert institution.is_active is True


def test_invalid_institution_type(db_session):
    institution = Institution(
        name="Instituição Inválida",
        institution_type="invalid",
    )

    db_session.add(institution)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_only_one_institution_can_own_local_stock(db_session):
    first_institution = Institution(
        name="UBS Teste 3",
        institution_type="ubs",
        is_local_stock_owner=True,
    )

    second_institution = Institution(
        name="UBS Teste 4",
        institution_type="ubs",
        is_local_stock_owner=True,
    )

    db_session.add(first_institution)
    db_session.commit()

    db_session.add(second_institution)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    assert db_session.scalar(
        select(func.count()).select_from(Institution)
    ) == 1


def test_multiple_institutions_without_local_stock_owner(db_session):
    first_institution = Institution(
        name="UBS Teste 5",
        institution_type="ubs",
    )

    second_institution = Institution(
        name="UBS Teste 6",
        institution_type="ubs",
    )

    db_session.add_all([first_institution, second_institution])
    db_session.commit()

    assert first_institution.id is not None
    assert second_institution.id is not None