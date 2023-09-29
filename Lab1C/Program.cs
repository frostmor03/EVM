using System;
using System.IO.Pipes;
using System.Runtime.CompilerServices;

public struct CustomData
{
    public int Number;
    public bool Flag;
}

class Client
{
    static void Main()
    {
        using (NamedPipeClientStream clientPipe = new(".", "Channel", PipeDirection.InOut))
        {
            clientPipe.Connect();

   
            byte[] receivedBytes = new byte[Unsafe.SizeOf<CustomData>()];
            clientPipe.Read(receivedBytes, 0, receivedBytes.Length);
            CustomData receivedData = Unsafe.As<byte, CustomData>(ref receivedBytes[0]);

            Console.WriteLine($"Number = {receivedData.Number}, Flag = {receivedData.Flag}");

            
            receivedData.Flag = true;


            byte[] modifiedBytes = Serialize(receivedData);
            clientPipe.Write(modifiedBytes, 0, modifiedBytes.Length);
        }
    }


    static byte[] Serialize(CustomData data)
    {
        byte[] bytes = new byte[Unsafe.SizeOf<CustomData>()];
        Unsafe.As<byte, CustomData>(ref bytes[0]) = data;
        return bytes;
    }
}
