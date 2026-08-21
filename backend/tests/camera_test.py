from vmbpy import VmbSystem

print('Hello, world')
with VmbSystem.get_instance() as vmb:
    cameras = vmb.get_all_cameras()

    print("Found:", len(cameras))

    for camera in cameras:
        print("ID:", camera.get_id())
        print("Model:", camera.get_model())
        print("Serial:", camera.get_serial())