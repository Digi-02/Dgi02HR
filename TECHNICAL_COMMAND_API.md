# Technical Command API

The HR application exposes a read-only workforce endpoint for Digi02 Technical Command:

```text
GET /api/v1/technical-command/people/
Authorization: Api-Key <TECHNICAL_COMMAND_API_KEY>
```

Today's live attendance is available separately:

```text
GET /api/v1/technical-command/attendance/today/
Authorization: Api-Key <TECHNICAL_COMMAND_API_KEY>
```

It returns one status per active employee (`checked_in`, `late`, `checked_out`, or `not_checked_in`), local check-in/check-out times, completed hours, and daily totals. It does not expose attendance history.

Configure `TECHNICAL_COMMAND_API_KEY` and `TECHNICAL_COMMAND_ORGANIZATION_SLUG` in the HR environment. Optional pagination settings are documented in `.env.example`.

Supported query parameters are `page`, `page_size`, `search`, `department`, and `ordering`. Ordering values are `name`, `employee_id`, `department`, `position`, and `updated_at`; prefix a value with `-` for descending order.

The endpoint returns active employees from only the configured organisation. It exposes work identity, department, position, manager, profile photo, employment category/status, non-empty technical skills, and update time. It intentionally excludes private contact, medical, identity, document, attendance, leave, and payroll data.

Use HTTPS in deployed environments, restrict network access where possible, and rotate both applications to a new matching key if a credential is exposed.
