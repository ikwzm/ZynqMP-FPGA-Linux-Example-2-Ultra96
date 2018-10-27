int negative(volatile int *in, volatile int *out, int size)

int main(){
    int data[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int result[10];
    int i;

    negative(data, result, 10);

    for(i = 0; i < 10; i++){
        printf("data[%d] = %d, result[%d] = %d\n", i, data[i], i, result[i]);
    }
}
