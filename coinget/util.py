def sortby_y_h(a, b):
    ay = a.rect.bottom + getattr(a, "height", 0)
    by = b.rect.bottom + getattr(b, "height", 0) 

    return cmp(ay, by)
