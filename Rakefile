
FPGA_BITSTREAM_FILE    = "negative.bin"
DEVICE_TREE_FILE       = "negative.dts"
DEVICE_TREE_NAME       = "negative"
DEVICE_TREE_DIRECTORY  = "/config/device-tree/overlays/#{DEVICE_TREE_NAME}"
UIO_DEVICE_NAMES       = ["negative-uio"]
UDMABUF_DEVICE_NAMES   = ["negative-udmabuf4", "negative-udmabuf5"]

def find_uio_device(name)
  found_device_name = nil
  Dir::entries("/sys/class/uio").map{ |device_name|
    if device_name =~ /^uio/
      File.open("/sys/class/uio/#{device_name}/name"){|file|
        if name.eql?(file.gets.chop)
          found_device_name = device_name
        end
      }
    end
  }
  return found_device_name
end

desc "Install fpga and devicetrees"
task :install => ["/lib/firmware/#{FPGA_BITSTREAM_FILE}", DEVICE_TREE_FILE] do
  begin
    sh "./dtbocfg.rb --install #{DEVICE_TREE_NAME} --dts #{DEVICE_TREE_FILE}"
  rescue => e
    print "error raised:"
    p e
    abort
  end
  if (Dir.exist?(DEVICE_TREE_DIRECTORY) == false)
    abort "can not #{DEVICE_TREE_DIRECTORY} installed."
  end

  UIO_DEVICE_NAMES.each do |device_name|
    device_file = find_uio_device(device_name)
    if (device_file.nil?)
      abort "can not find uio device file named #{device_name}"
    end
    if (File.exist?("/dev/" + device_file) == false)
      abort "can not /dev/#{device_file} installed."
    end
    File::chmod(0666, "/dev/" + device_file)
  end    

  UDMABUF_DEVICE_NAMES.each do |device_file|
    if (File.exist?("/dev/" + device_file) == false)
      abort "can not /dev/#{device_file} installed."
    end
    File::chmod(0666, "/dev/" + device_file)
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_mode")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_offset")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_size")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_direction")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_owner")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_for_cpu")
    File::chmod(0666, "/sys/class/udmabuf/" + device_file + "/sync_for_device")
  end
end

desc "Uninstall fpga and devicetrees"
task :uninstall do
  if (Dir.exist?(DEVICE_TREE_DIRECTORY) == false)
    abort "can not #{DEVICE_TREE_DIRECTORY} uninstalled: does not already exists."
  end
  sh "./dtbocfg.rb --remove #{DEVICE_TREE_NAME}"
end

file "/lib/firmware/#{FPGA_BITSTREAM_FILE}" => ["#{FPGA_BITSTREAM_FILE}"] do
  sh "cp #{FPGA_BITSTREAM_FILE} /lib/firmware/#{FPGA_BITSTREAM_FILE}"
end

directory DEVICE_TREE_DIRECTORY do
  Rake::Task["install"].invoke
end

