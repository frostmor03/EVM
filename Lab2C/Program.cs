using System;
using System.IO.Pipes;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

public struct Structure
{
    public int Number;
    public bool Flag;
}

class Client
{
    static async Task Main()
    {
        using (NamedPipeClientStream client = new NamedPipeClientStream(".", "Сhannel", PipeDirection.InOut))
        {
            await client.ConnectAsync();
            Console.WriteLine("Подключено");
            try
            {
                while (true)
                {
                    byte[] bytes = new byte[Unsafe.SizeOf<Structure>()];
                    await client.ReadAsync(bytes, 0, bytes.Length);
                    Structure receivedData = Unsafe.As<byte, Structure>(ref bytes[0]);
                    Console.WriteLine($"Полученные данные: Число = {receivedData.Number}, Флаг = {receivedData.Flag}");

                    // Просто отправляем принятое число обратно
                    byte[] modifiedBytes = new byte[Unsafe.SizeOf<Structure>()];
                    Unsafe.As<byte, Structure>(ref modifiedBytes[0]) = receivedData;
                    
                    await client.WriteAsync(modifiedBytes, 0, modifiedBytes.Length);
                }
            }
            catch (Exception) { }
        }
    }
}