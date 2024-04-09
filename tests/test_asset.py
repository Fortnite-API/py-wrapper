import fortnite_api

V_BUCK_ICON_URL: str = "https://fortnite-api.com/images/vbuck.png"


def test_asset():
    with fortnite_api.SyncFortniteAPI() as client:

        mock_asset = fortnite_api.Asset(http=client.http, url=V_BUCK_ICON_URL)

    assert mock_asset.url == V_BUCK_ICON_URL
    assert mock_asset.can_resize is False
    assert mock_asset._max_size is fortnite_api.utils.MISSING
    assert mock_asset.max_size == -1

    try:
        mock_asset.resize(256)
        assert False, "Should not be able to resize this asset."
    except ValueError:
        pass

    mock_asset._max_size = 256
    assert mock_asset.can_resize is True
    assert mock_asset._max_size == 256
    assert mock_asset.max_size == 256

    # Asset that you cannot resize to something that isn't a power of 2
    try:
        mock_asset.resize(255)
        assert False, "Should not be able to resize this asset to a non-power of 2."
    except TypeError:
        pass

    # Ensure that you cannot resize to something bigger than the max size
    try:
        mock_asset.resize(512)
        assert False, "Should not be able to resize this asset to a size bigger than the max size."
    except ValueError:
        pass

    assert mock_asset._size is fortnite_api.utils.MISSING

    # Resize this asset and ensure it copies right
    resized = mock_asset.resize(8)
    assert resized is mock_asset
    assert resized._max_size == mock_asset._max_size
    assert resized.max_size == mock_asset.max_size
    assert resized._size == 8
    assert resized.url == f"{V_BUCK_ICON_URL[:-4]}_8.png"

    # Now finally make sure that if the max size is None, you can resize to anything
    mock_asset._max_size = None
    assert mock_asset.can_resize is True
    assert mock_asset._max_size is None
    assert mock_asset.max_size is None
