/**
 * Tipos mínimos de Web Bluetooth (no está en lib.dom).
 */

interface BluetoothRemoteGATTCharacteristicLike extends EventTarget {
  value: DataView | null;
  startNotifications(): Promise<BluetoothRemoteGATTCharacteristicLike>;
  writeValue(data: BufferSource): Promise<void>;
}

interface BluetoothRemoteGATTServiceLike {
  getCharacteristic(uuid: string): Promise<BluetoothRemoteGATTCharacteristicLike>;
}

interface BluetoothRemoteGATTServerLike {
  connected: boolean;
  connect(): Promise<BluetoothRemoteGATTServerLike>;
  disconnect(): void;
  getPrimaryService(uuid: string): Promise<BluetoothRemoteGATTServiceLike>;
}

interface BluetoothDeviceLike extends EventTarget {
  name?: string;
  gatt?: BluetoothRemoteGATTServerLike;
}

interface BluetoothLike {
  requestDevice(options: {
    filters?: { services?: string[]; name?: string }[];
    optionalServices?: string[];
  }): Promise<BluetoothDeviceLike>;
}

interface Navigator {
  bluetooth?: BluetoothLike;
}
