# ca-lib Utilities Reference

Shared utilities available from ca-lib.

---

## gRPC Utilities

```python
from ca_lib.grpc.decorators import ca_user_service_authenticated
from ca_lib.grpc.exceptions import InvalidRequestArgumentsException
```

## Django Integration

```python
from ca_lib.djangolib.models import base
from ca_lib.djangolib.fields import ProtobufEnumField
```

## Datetime Handling

```python
from ca_lib import clover_datetime
now = clover_datetime.CloverDatetime.now()
```

## Protocol Buffers

```python
from ca_lib.ca_lib_protocols import constants_pb2
```

---

*Related: See skill.md for complete utilities*
