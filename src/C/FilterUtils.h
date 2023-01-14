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

#ifndef FILTERH
#define FILTERH

/*
LTI filter (see "namingconventions.pdf")
*/
typedef struct _Filter{
    // Numerator coefficients (x[n-i])
    float* a;
    // Denominator coefficients (y[n-i])
    float* b;
    unsigned short length;
    // State vector
    float* w;
    // Current position (used for rolling the values without changing the vector)
    unsigned short current;
}Filter;

// Applies the non-recursive part of the filter (a)
float applyFIR(Filter* filter, float x);

// Applies the whole filter
float applyIIR(Filter* filter, float x);

// Constructs a filter structure
Filter* filter_c(float* a, float* b, unsigned short length);

// Memory management
void free_filter(Filter** f);

#endif