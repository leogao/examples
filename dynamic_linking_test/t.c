#include <stdio.h>
#include <dlfcn.h>

int main ()
{
  void *h = dlopen ("./foo.so", RTLD_LAZY|RTLD_GLOBAL);
  void *p = dlsym (h, "bar");

  printf ("h = %p, p = %p\n", h, p);

  dlclose (h);

  h = dlopen ("./foo.so", RTLD_LAZY|RTLD_GLOBAL);
  p = dlsym (h, "bar");
  printf ("h = %p, p = %p\n", h, p);

  return 0;
}

