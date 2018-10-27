from udmabuf import Udmabuf
from uio     import Uio
import numpy as np
import time

if __name__ == '__main__':
    uio1       = Uio('uio1')
    regs       = uio1.regs()
    udmabuf4   = Udmabuf('udmabuf4')
    udmabuf5   = Udmabuf('udmabuf5')
    test_dtype = np.uint32
    test_size  = min(int(udmabuf4.buf_size/(np.dtype(test_dtype).itemsize)),
                     int(udmabuf5.buf_size/(np.dtype(test_dtype).itemsize)))
  
    udmabuf4_array    = udmabuf4.memmap(dtype=test_dtype, shape=(test_size))
    udmabuf4_array[:] = np.random.randint(-21474836478,2147483647,(test_size))
    udmabuf4.set_sync_to_device(0, test_size*(np.dtype(test_dtype).itemsize))

    udmabuf5_array    = udmabuf5.memmap(dtype=test_dtype, shape=(test_size))
    udmabuf5_array[:] = np.random.randint(-21474836478,2147483647,(test_size))
    udmabuf5.set_sync_to_cpu(   0, test_size*(np.dtype(test_dtype).itemsize))

    total_setup_time   = 0
    total_cleanup_time = 0
    total_xfer_time    = 0
    total_xfer_size    = 0
    count              = 0

    for i in range (0,9):

        start_time  = time.time()
        udmabuf4.sync_for_device()
        udmabuf5.sync_for_device()
        regs.write_word(0x18, udmabuf4.phys_addr & 0xFFFFFFFF)
        regs.write_word(0x20, udmabuf5.phys_addr & 0xFFFFFFFF)
        regs.write_word(0x28, test_size)
        regs.write_word(0x04, 0x000000001)
        regs.write_word(0x08, 0x000000001)
        regs.write_word(0x0C, 0x000000001)
        uio1.irq_on()
        phase0_time = time.time()
        regs.write_word(0x00, 0x000000001)
        uio1.wait_irq()

        phase1_time = time.time()
        regs.write_word(0x0C, 0x000000001)
        udmabuf4.sync_for_cpu()
        udmabuf5.sync_for_cpu()

        end_time     = time.time()
        setup_time   = phase0_time - start_time
        xfer_time    = phase1_time - phase0_time
        cleanup_time = end_time    - phase1_time
        total_time   = end_time    - start_time

        total_setup_time   = total_setup_time   + setup_time
        total_cleanup_time = total_cleanup_time + cleanup_time
        total_xfer_time    = total_xfer_time    + xfer_time
        total_xfer_size    = total_xfer_size    + test_size
        count              = count              + 1
        print ("total:{0:.3f}[msec] setup:{1:.3f}[msec] xfer:{2:.3f}[msec] cleanup:{3:.3f}[msec]".format(round(total_time*1000.0,3), round(setup_time*1000.0,3), round(xfer_time*1000.0,3), round(cleanup_time*1000.0,3)))


    print ("average_setup_time  :{0:.3f}".format(round((total_setup_time  /count)*1000.0,3)) + "[msec]")
    print ("average_cleanup_time:{0:.3f}".format(round((total_cleanup_time/count)*1000.0,3)) + "[msec]")
    print ("average_xfer_time   :{0:.3f}".format(round((total_xfer_time   /count)*1000.0,3)) + "[msec]")
    print ("throughput          :{0:.3f}".format(round(((total_xfer_size/total_xfer_time)/(1000*1000)),3)) + "[MByte/sec]")

    udmabuf4_negative_array = np.negative(udmabuf4_array)
    if np.array_equal(udmabuf4_negative_array, udmabuf5_array):
         print("np.negative(udmabuf4) == udmabuf5 : OK")
    else:
         print("np.negative(udmabuf4) == udmabuf5 : NG")
         count = 0
         for i in range(test_size):
             if udmabuf4_negative_array[i] != udmabuf5_array[i] :
                 count = count + 1
                 if count < 16:
                     print("udmabuf4_negative_array[0x{0:08X}] = 0x{1:08X} udmabuf5_array[0x{0:08X}] = 0x{2:08X}".format(i, udmabuf4_negative_array[i], udmabuf5_array[i]))
         print("NG Count:{0}".format(count))
         
    
