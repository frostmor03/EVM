using System;
using System.IO.Pipes;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

public struct Structure
{
    public int Number;
    public bool Flag;
}

class PipeServer
{
    private PriorityQueue<Structure, int> dataQueue = new PriorityQueue<Structure, int>();
    private Mutex mutex = new Mutex();
    private string str = string.Empty; 

    public async Task RunServerAsync()
    {
        CancellationTokenSource source = new CancellationTokenSource();
        CancellationToken token = source.Token;
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream("Сhannel", PipeDirection.InOut))
        {
            Console.WriteLine("Ожидание подключения клиента...");
            await pipeServer.WaitForConnectionAsync();
            string fileName = "output.txt";
            Console.WriteLine("Клиент подключен");

            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                source.Cancel();
                SaveToFile(fileName, str);
            };

            await Task.WhenAll(SenderTask(pipeServer, token), ReceiverTask(pipeServer, token));
        }
    }

    private async Task SenderTask(NamedPipeServerStream pipeServer, CancellationToken token)
    {
        await Task.Run(async () =>
        {
            while (!token.IsCancellationRequested)
            {
                int _Number, _priority;
                bool _Flag;
                Console.Write("Введите число: ");
                int.TryParse(Console.ReadLine(), out _Number);
                Console.Write("Введите флаг: ");
                bool.TryParse(Console.ReadLine(), out _Flag);
                Console.Write("Введите приоритет: ");
                if (!int.TryParse(Console.ReadLine(), out _priority))
                    _priority = 0;

                Structure data = new Structure
                {
                    Number = _Number,
                    Flag = _Flag,
                };

                mutex.WaitOne();
                dataQueue.Enqueue(data, _priority);
                mutex.ReleaseMutex();
            }
        });
    }

    private async Task ReceiverTask(NamedPipeServerStream pipeServer, CancellationToken token)
    {
        while (!token.IsCancellationRequested)
        {
            Structure st;
            int pr;
            mutex.WaitOne();
            bool flag = dataQueue.TryDequeue(out st, out pr);
            mutex.ReleaseMutex();
            if (flag)
            {
                byte[] dataBytes = new byte[Unsafe.SizeOf<Structure>()];
                Unsafe.As<byte, Structure>(ref dataBytes[0]) = st;
                await pipeServer.WriteAsync(dataBytes, 0, dataBytes.Length);
                byte[] receivedBytes = new byte[Unsafe.SizeOf<Structure>()];
                if (await pipeServer.ReadAsync(receivedBytes, 0, receivedBytes.Length) == receivedBytes.Length)
                {
                    st = Unsafe.As<byte, Structure>(ref receivedBytes[0]);
                }
                str += $"Число = {st.Number}; Флаг = {st.Flag}; Приоритет = {pr}\n";
            }
        }
    }

    private static void SaveToFile(string name, string str)
    {
        File.AppendAllText(name, str);
    }
}

class Program
{
    static async Task Main()
    {
        PipeServer server = new PipeServer();
        await server.RunServerAsync();
    }
}
