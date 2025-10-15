using System.Collections.Generic;
using DiKErnel.Core;

namespace LogHandlerHelper
{
    public class LogHandler : ILogHandler
    {
        private readonly List<string> warnings = new List<string>();
        private readonly List<string> errors = new List<string>();

        public IReadOnlyList<string> Warnings => warnings;

        public IReadOnlyList<string> Errors => errors;

        public void Clear()
        {
            warnings.Clear();
            errors.Clear();
        }

        public void LogWarning(string message) => warnings.Add(message);

        public void LogError(string message) => errors.Add(message);
    }
}
