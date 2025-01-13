using System.Text.Json;

namespace Loader
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: JsonLoader <path-to-json-file>");
                return;
            }

            var filePath = args[0];

            if (!File.Exists(filePath))
            {
                Console.WriteLine($"Error: File '{filePath}' not found.");
                return;
            }

            try
            {
                var jsonContent = File.ReadAllText(filePath);
                var rootObject = JsonSerializer.Deserialize<CardList>(jsonContent, new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    WriteIndented = true
                });

                Console.WriteLine("JSON file loaded successfully!");
                Console.WriteLine("Displaying data:");
                Console.WriteLine(JsonSerializer.Serialize(rootObject, new JsonSerializerOptions { WriteIndented = true }));
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error loading JSON: {ex.Message}");
            }
        }
    }

    ///<summary>
    ///     A Card List used to store Baseball Card information
    ///</summary>
    public class CardList
    {
        /// <summary>
        ///     Attributes that will be used on the Baseball Cards that are part of this JSON File
        /// </summary>
        [JsonPropertyName("attributes")]
        public List<AttributeItem> Attributes { get; set; }

        /// <summary>
        ///     Sets of Baseball Cards that are part of this JSON File
        /// </summary>
        [JsonPropertyName("sets")]
        public List<Set> Sets { get; set; }
    }

    /// <summary>
    ///     Defines an attribute that can be used on a Baseball Card (such as Rookie Card, Autograph, etc.)
    /// </summary>
    public class AttributeItem
    {
        /// <summary>
        ///     String used to define the attribute (usually an abbreviation such as "RC" for Rookie Card, etc.)
        /// </summary>
        [JsonPropertyName("attribute")]
        public string Attribute { get; set; }

        /// <summary>
        ///     Notes or additional information about the attribute
        /// </summary>
        [JsonPropertyName("note")]
        public string Note { get; set; }
    }

    /// <summary>
    ///     Defines a set of Baseball Cards
    /// </summary>
    public class Set
    {
        /// <summary>
        ///     Name of the set
        /// </summary>
        [JsonPropertyName("name")]
        public string Name { get; set; }

        /// <summary>
        ///     Notes or additional information about the set
        /// </summary>
        [JsonPropertyName("notes")]
        public List<string> Notes { get; set; }

        /// <summary>
        ///     Variations that apply to the entire set (misprinting that affect all cards in the set, etc.)
        /// </summary>
        [JsonPropertyName("variations")]
        public List<Variation> Variations { get; set; }

        /// <summary>
        ///     Parallel versions of the set (such as a Gold parallel, etc.)
        /// </summary>
        [JsonPropertyName("parallels")]
        public List<Parallel> Parallels { get; set; }

        /// <summary>
        ///     List of Baseball Cards that are part of this set
        /// </summary>
        [JsonPropertyName("cards")]
        public List<Card> Cards { get; set; }
    }

    /// <summary>
    ///     Variation of a set/card (such as a misprint, error, etc.)
    /// </summary>
    public class Variation
    {
        /// <summary>
        ///    Name/Title of the variation
        /// </summary>
        [JsonPropertyName("variation")]
        public string VariationName { get; set; }

        /// <summary>
        ///     Notes or additional information about the variation
        /// </summary>
        [JsonPropertyName("note")]
        public string Note { get; set; }
    }

    /// <summary>
    ///     Parallel Set of a set/card (such as a Gold parallel, etc.)
    /// </summary>
    public class Parallel
    {
        /// <summary>
        ///     Name/Title of the Parallel
        /// </summary>
        [JsonPropertyName("name")]
        public string Name { get; set; }

        /// <summary>
        ///     Number of cards in the parallel set (if limited printing run)
        /// </summary>
        [JsonPropertyName("of")]
        public int? Of { get; set; }

        /// <summary>
        ///     Notes or additional information about the parallel set
        /// </summary>
        [JsonPropertyName("notes")]
        public List<string> Notes { get; set; }
    }

    /// <summary>
    ///     Represents a Baseball Card
    /// </summary>
    public class Card
    {
        /// <summary>
        ///     Number of the card (if any)
        /// </summary>
        [JsonPropertyName("number")]
        public string Number { get; set; }

        /// <summary>
        ///     Name of the player or subject of the card
        /// </summary>
        [JsonPropertyName("name")]
        public string Name { get; set; }

        /// <summary>
        ///     Any additional attributes that apply to this card (such as Rookie Card, Autograph, etc.)
        /// </summary>
        [JsonPropertyName("attributes")]
        public List<string> Attributes { get; set; }

        /// <summary>
        ///     Notes or additional information about the card
        /// </summary>
        [JsonPropertyName("note")]
        public string Note { get; set; }

        /// <summary>
        ///     Variations that apply to this card (misprinting that affect this card, etc.)
        /// </summary>
        [JsonPropertyName("variations")]
        public List<Variation> Variations { get; set; }

        /// <summary>
        ///     Parallel versions of this card (such as a Gold parallel, etc.) that apply to just this card (not the entire set)
        /// </summary>
        [JsonPropertyName("parallels")]
        public List<Parallel> Parallels { get; set; }
    }
}
