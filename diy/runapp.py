#!/usr/bin/env python
import os

import main

if __name__ == "__main__":
    port = os.environ['OPENSHIFT_INTERNAL_PORT']
    address = os.environ['OPENSHIFT_INTERNAL_IP']
    main.run(port,address)

