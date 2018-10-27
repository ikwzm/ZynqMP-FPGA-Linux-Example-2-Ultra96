int negative(volatile int *in, volatile int *out, int size){
#pragma HLS INTERFACE m_axi depth=10 port=out offset=slave
#pragma HLS INTERFACE m_axi depth=10 port=in  offset=slave
#pragma HLS INTERFACE s_axilite port=size
#pragma HLS INTERFACE s_axilite port=return
    int i;

    for (i = 0; i < size; i++){
        out[i] = -in[i];
    }

    return(0);
}
