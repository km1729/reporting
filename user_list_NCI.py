import grp

info = grp.getgrnam('dp9')
members = info.gr_mem