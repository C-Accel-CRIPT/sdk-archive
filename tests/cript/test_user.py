"""
Test for CRIPT User node

"""
from cript import User


def test_initialization():
    user_node = User(
        name="Dylan Walsh",
        email="dylanwal@mit.edu",
        organization="Mass. Institute of Technology",
        position="Postdoc"
    )

    assert isinstance(user_node, User)
