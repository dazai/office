# -*- coding: utf-8 -*-
import icu

collator = icu.Collator.createInstance(icu.Locale('ar_utf8'))

l = ['ا', 'ب', 'پ', 'ح', 'س', 'ص', 'ف', 'ک', 'ک', 'ک', 'م', 'م']
# ش ا ه د ة ج م  ع م و ا
print(sorted(l, key=collator.getSortKey))
