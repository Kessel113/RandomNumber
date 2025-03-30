from proc_img import get_data_for_base
from base_data import BaseData
from seed_data import SeedData
from radio import get_data_for_seed
from generator import generate
from audio_entropy import calculate_entropy  # Ensure this function exists

def main():
    base_data_string = get_data_for_base()
    base = BaseData(base_data_string)
    count = 1
    total_numbers = 10000  # Target amount
    batch_size = 2000  # Generate numbers in batches

    entropy_values = []  # Store entropy values for analysis

    seed_data_string = get_data_for_seed()
    seed = SeedData(seed_data_string)

    with open('numbers.txt', 'ab') as file:
        for _ in range(total_numbers // batch_size):              
            batch_data = bytearray()  # Store generated batch for entropy check
            for _ in range(batch_size):
                rand_num = generate(base.get_base(), seed.get_seed(), 1, 65530, count)
                count += 1
                file.write(rand_num.to_bytes(2, byteorder="big"))
                batch_data.extend(rand_num.to_bytes(2, byteorder="big"))  # Collect bytes

                if seed.about_to_finish() == True:  
                    print("Data from radio has been exhausted. Fetching new data...")
                    seed.update_data(get_data_for_seed())

            # Calculate entropy of this batch
            entropy = calculate_entropy(batch_data)
            entropy_values.append(entropy)
            print(f"Batch entropy: {entropy:.5f}")

    # Compute entropy statistics
    if entropy_values:
        peak_entropy = max(entropy_values)
        low_entropy = min(entropy_values)
        avg_entropy = sum(entropy_values) / len(entropy_values)

        print("\n🔹 **Entropy Report** 🔹")
        print(f"✅ Peak Entropy: {peak_entropy:.5f} bits/byte")
        print(f"⚠️ Low Entropy: {low_entropy:.5f} bits/byte")
        print(f"📊 Average Entropy: {avg_entropy:.5f} bits/byte")

if __name__ == "__main__":
    main()
