# Development Journal

This document records the challenges I faced while developing the Trek Management System and the lessons I learned while solving them.

---

## Challenge 1: Understanding `data.get()` vs `data[]`

While implementing the user registration API, I initially accessed request data using dictionary indexing:

```python
data['name']
```

I learned that this raises a `KeyError` if the client does not send the required field.

To avoid this, I explored the use of:

```python
data.get('name')
```

Unlike dictionary indexing, `get()` safely returns `None` when the key is missing instead of raising an exception. This allowed me to validate incoming request data before accessing it.