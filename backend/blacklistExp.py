import re

regex_blacklistExp = [
    r"(?i)(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})",
    r"(?i)((<script|script>)|(bot)|(\.\.\/))",
]