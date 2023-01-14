/*
    FilterUtils - LTI filter utility functions
    Copyright (C) 2023 Amélia O. F. da Silva

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
#include <stdlib.h>
#include "FilterUtils.h"

/*
Travels backwards (from «start») through vals, accumulating
the products between those and a forward traversal of coefs

prod_sum [a,b,c,d] [0,1,2,3] 2 = [0c,1b,2a,3d]

*/
float r_prod_sum(
    float* coefs,
    float* vals,
    unsigned short start,
    unsigned short val_length
){
    short i=(start+val_length)%val_length;
    unsigned short n=0;
    float acc=0;
    do
    {
        acc+=coefs[n]*vals[i];
        // We advance one step and loop back to the beginning
        n++;
        i--;
        i=(i+val_length)%val_length;
    }
    while(i!=start);
    return acc;
}

float applyFIR_to_curr_state(Filter* filter)
{
    float y = r_prod_sum(
        filter->a,
        filter->w,
        filter->current,
        filter->length
    );
    //Go to the next position
    filter->current++;
    filter->current%=filter->length;
    return y;
}

float applyFIR(Filter* filter, float x)
{
    filter->w[filter->current]=x; // Assign the current state
    return applyFIR_to_curr_state(filter);
}

float applyIIR(Filter *filter, float x)
{
    filter->w[filter->current]= x+r_prod_sum(
        filter->b,
        filter->w,
        filter->current+1,
        filter->length
    );// Assign the current state
    return applyFIR_to_curr_state(filter);
}

Filter *filter_c(float *a, float *b, unsigned short length)
{
    Filter* f = malloc(sizeof(Filter));
    f->a=a;
    f->b=b;
    f->current=0;
    f->length=length;
    f->w=calloc(length,sizeof(float));
    return f;
}

void free_filter(Filter** f)
{
    free((*f)->w);
    free(*f);
    *f=0;
}