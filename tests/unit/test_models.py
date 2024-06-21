from main.data.models import Feed


# Test to ensure a new record can be created from the models imported
def test_new_feed(new_feed):
    """
    GIVEN a Feed model
    WHEN a new Feed is created
    THEN check that a new id is generated
    """
    assert new_feed.name == 'BOM'
    assert new_feed.location == 'sydney'
    assert new_feed.category == 'weather'
    assert new_feed.url == 'http://weather'
    assert type(new_feed.id) is int

