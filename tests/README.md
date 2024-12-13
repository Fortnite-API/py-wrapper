# Fortnite API Library Tests

This library makes a large effort to ensure that the responses given from the API are stably transformed to their
respective Python objects. Every client, both in the `Client` and `SyncClient` classes are tested. This file
outlines how the tests are laid such that all these edge cases are handled.

## Generic Library Tests

Many tests in the main `/tests` directory are generic-related object-related tests. These ensure basic functionality surrounding how the more-complex objects of the library are constructed and function.

| Test File             | Purpose and Logic                                                                                                                                                                      |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_account.py`     | Ensures that an `Account` object is created properly and its dunder methods work as expected.                                                                                          |
| `test_aes.py`         | Ensures that `Aes` object initializes properly by checking known dynamic keys and hashes.                                                                                              |
| `test_asset.py`       | Ensures that the rules regulating `Asset` resizing are correct and that the asset reading functions function correctly.                                                                |
| `test_beta.py`        | Ensures that a user with the `beta` flag disabled on a `Client` cannot call beta methods. This validates that the beta flag decorator works as expected.                               |
| `test_proxy.py`       | Ensures that the `TransformerListProxy` class initializes properly, transforms to expected objects as needed, and has the same interface as a typical `py.List` would.                 |
| `test_ratelimits.py`  | Ensures that the library's handling of rate limits is correct, and related exceptions are raised as expected.                                                                          |
| `test_reconstruct.py` | Ensures that the `Reconstructable` class correctly recreates the class it wraps.                                                                                                       |
| `test_repr.py`        | The library uses a dynamic decorator to create the `__repr__` dunder by taking advantage of the `__slots__` on a class. This test ensures that the dynamic function works as expected. |
| `test_methods.py`     | The handling of all the functions on the `Client` and `SyncClient` class. See Edge Cases below for more information. |

### Edge Case Library Tests

#### Definition and Tests for the Hybrid Client

##### Test Client Hybrid: `test_client_hybrid.py`

The tests define a custom `ClientHybrid` class (in `./client/test_client_hybrid.py`). This class wraps a `Client` to act as an intermediatory between a requested API call and the actual method. All tests that make API calls will import the `ClientHybrid`.

As an example, consider the user requesting to call `fetch_aes()` using the `ClientHybrid`:

- The sync method of `fetch_aes()` is called on an internally held `SyncClient` class.
- The async method of `fetch_aes()` is called on the `Client` itself.
- The result, if reconstructable or comparable, is checked to ensure that both returned objects are the same.
- The result of the async method call is returned as the final value.

This approach, although "blocking" in nature, ensures that the results from both the `Client` and `SyncClient` are the same.

##### Test Client: `test_client.py`

The tests defined here ensure that the client's behavior surrounding initialization work as expected. This is, but is not limited to, context manager use, custom passed HTTP session management, etc.

#### Tests for the Methods on the Client

Every method, except for those defined in `test_stats.py` and `cosmetics/*.py` (more on this directory after) on the `Client` is tested here. This uses the `ClientHybrid`, as described above.

This logic has been separated out of the conventional cosmetic tests due to the nature of the stats endpoints themselves. The `Client` must have API key while using them, unlike any other endpoint, and have been clustered together accordingly.

#### Cosmetic Tests: `/cosmetics/*.py`

A majority of the definitions in this library relate to the cosmetics of Fortnite. Thus, the tests for them are inherently large. To combat this, and to future proof the readability and maintainability of the library, these tests have been separated from others of the `Client` to `cosmetics/test_cosmetic_functions.py` and the associated internal helper functions to `cosmetics/cosmetic_utils.py`.
