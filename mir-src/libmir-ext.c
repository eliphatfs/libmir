#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include "mir.h"


MIR_module_t MIR_get_last_module (MIR_context_t ctx) {
  return DLIST_TAIL (MIR_module_t, *MIR_get_module_list (ctx));
}

MIR_module_t MIR_get_module (MIR_context_t ctx, const char *name) {
  MIR_module_t module, next_module;

  for (module = DLIST_HEAD (MIR_module_t, *MIR_get_module_list (ctx)); module != NULL;
       module = next_module) {
    next_module = DLIST_NEXT (MIR_module_t, module);
    if (strcmp(module->name, name) == 0)
      return module;
  }
  return NULL;
}

MIR_item_t MIR_get_export_item (MIR_context_t ctx, const char *name, MIR_module_t module) {
  for (MIR_item_t item = DLIST_HEAD (MIR_item_t, module->items); item != NULL;
       item = DLIST_NEXT (MIR_item_t, item)) {
    if (item->item_type == MIR_export_item && strcmp (item->u.export_id, name) == 0) {
      return item->ref_def;
    }
  }
  return NULL;
}

int MIR_vsnprintf(char * buffer, unsigned int n, const char * format, va_list varg)
{
    return vsnprintf(buffer, n, format, varg);
}
