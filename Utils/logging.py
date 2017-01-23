#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, logstash_formatter

class LogFormatter(logstash_formatter.LogstashFormatterV1):
    def format(self, record):
        if record.name == 'tornado.access' and len(record.args) == 3:
            p = re.compile(r"^([A-Z]+) (.+) \((.+)\)$")
            m = p.match(record.args[1])
            if m is not None:
                record.method, record.path, record.ipAddress = m.group(1, 2, 3)
            # Cleanup Args
            record.msg = record.msg % record.args
            record.args = None
        return super(LogFormatter, self).format(record)
