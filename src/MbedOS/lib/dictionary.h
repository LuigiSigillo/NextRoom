#ifndef couple_t
typedef struct
{
    char* key;
    int value;
} couple_t;
#endif

#ifndef dictionary_t
typedef struct
{
    couple_t dict[50];
    int size;
} dictionary_t;
#endif