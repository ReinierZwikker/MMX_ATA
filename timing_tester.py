"""
Test the timing difference to the first note between wav files in the input folder. It will detect a threshold change in volume as a note played and
then output the differences between the first notes of all the files. If the time difference between adding spacers to channels is measured,
the program could be altered to advise a number of washers to add or remove.

The program will then calculate the consistency of each input by measuring the timing between the start of each note.

For better explanation, see README.md

Written by Suddenly for martin and the mmx
"""
try:
    import warnings
    from numpy import average, std
    from scipy.io.wavfile import read as wav_read
    from os import listdir
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy and wave package before running.")
    raise SystemExit

# ----- SETTINGS -----

volume_threshold = 254  # Wave value difference
minimal_note_spacing = 10000  # samples between notes to catch duplicates
input_files_folder = "input_files"


# ----- FUNCTIONS -----


def get_min_index(lst):
    # returns the index of the lowest value of lst
    min_index = 0
    for index in range(len(lst)):
        if lst[index] <= lst[min_index]:
            min_index = index
    return min_index


# ----- CLASSES -----

class Channel:

    def __init__(self, channel_file_name):
        self.file_name = channel_file_name
        self.file_name_formatted = channel_file_name[:-4].capitalize()
        try:
            # Ignoring warnings here because SciPy warns if it finds non-data block, like the header, which is not a problem for us
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.sample_rate, self.frames_array = wav_read("./" + input_files_folder + "/" + channel_file_name)
                # The time that each sample takes is the reciprocal of the sample rate
                self.timing = 1 / self.sample_rate
        except FileNotFoundError:
            print("Oops, I thought I found a file, but it seems it does not exist... \nIf you are seeing this, something went pretty wrong, "
                  "but i'm continuing anyway")
        self.note_indices = self.get_note_indices()

        # The first time we want all the notes timing from the start of the list
        self.note_framing_list = self.get_note_framing_list(0)
        self.note_timing_list = self.get_note_timing_list(self.note_framing_list)

    def get_note_indices(self):
        note_indices = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for frame_index in range(1, len(self.frames_array)):
                difference = abs(self.frames_array[frame_index - 1] - self.frames_array[frame_index])
                if len(note_indices) > 0:
                    spacing = frame_index - note_indices[-1]
                else:
                    spacing = minimal_note_spacing + 1
                if difference > volume_threshold and spacing > minimal_note_spacing:
                    note_indices.append(frame_index)
            if len(note_indices) == 0:
                print("ERROR, empty track found. Please adjust parameters or remove track")  # TODO ignore empty tracks
                raise SystemExit
            return note_indices

    def get_note_framing_list(self, reference_index):
        note_framing_list = []
        for note_index in self.note_indices:
            note_framing_list.append((note_index - reference_index))
        return note_framing_list

    def get_note_timing_list(self, note_framing_list):
        return [self.get_note_timing(frame_index) for frame_index in note_framing_list]

    def get_note_timing(self, frame_index):
        return self.timing * frame_index

    def print_notes_found(self, reference_index):
        self.get_note_timing_list(self.get_note_framing_list(reference_index))
        print("\n", self.file_name_formatted)
        for i in range(len(self.note_indices)):
            print(f"\nNote #{str(i + 1)}: {self.note_timing_list[i]} s")


# ----- PROGRAM -----

print("\n\n\tWelcome to the MMX timing analysing utility!")

print("\n\tWritten by Suddenly for Martin and the MMX Team!\n")

print(f"\nUsing {volume_threshold} as volume threshold and {minimal_note_spacing} samples as minimal note spacing.")

print("\nLoading files...")

try:
    # To read the files, we first need to find their names
    folder_files = listdir("./" + input_files_folder)
except FileNotFoundError:
    print(f"\nCould not find the '{input_files_folder}' folder. Please put your input files in before running!")
    raise SystemExit

if len(folder_files) > 0:
    print("\n\t", len(folder_files), "files loaded!")
else:
    print(f"\nCouldn't find any files! Please put the input files in a subfolder called '{input_files_folder}' next to the python file")
    raise SystemExit

# Check if all the files are actually wave files
file_names = []
for folder_file in folder_files:
    if folder_file.endswith(".wav"):
        file_names.append(folder_file)
    else:
        print(f"WARNING: Please only put .wav files in the input folder, skipping {folder_file}")

print("\nAnalysing data...")

# Create a Channel object for each file in the folder and load that wave file into the object
channel_list = []
for file_name in file_names:
    channel_list.append(Channel(file_name))

print("\n\n\n\t Results:\n\n\nDetected notes:")

# print the all notes found with their time wrt the begin of the file
for channel in channel_list:
    channel.print_notes_found(0)

print("\n\n\n\t Machine timing:")

# Create 3 new lists, the placement of all notes and then a copy of this list and a copy of the name list, to edit for the sorting process
first_note_times = []
file_name_formatted_sorting = []
for channel in channel_list:
    first_note_times.append(channel.note_timing_list[0])
    file_name_formatted_sorting.append(channel.file_name_formatted)
first_note_times_sorting = first_note_times

# Detect the first note and use that as reference
channel_index = get_min_index(first_note_times_sorting)
reference_time = first_note_times_sorting[channel_index]

print("\n\nThe first channel is", file_name_formatted_sorting[channel_index],
      f"\nThe first note is  {first_note_times_sorting[channel_index]} s from the start of the file")

# Remove this entry from the sorting list, as we already had it.
first_note_times_sorting.pop(channel_index)
file_name_formatted_sorting.pop(channel_index)

# Repeat this process of displaying the first note until there are no notes left.
while len(first_note_times_sorting) > 0:
    channel_index = get_min_index(first_note_times_sorting)
    print("\n\nThe next channel is", file_name_formatted_sorting[channel_index],
          f"\nThis channel is {first_note_times_sorting[channel_index] - reference_time} s later than the first channel")
    first_note_times_sorting.pop(channel_index)
    file_name_formatted_sorting.pop(channel_index)

print("\n\n\n\t Channel consistency:")

# Calculate the consistency of each channel by making a list of the time between each note and giving the avg and st_dev of that list. This will
# show if the channel is actually playing a note every beat and if the interval is consistent.
for channel in channel_list:
    print("\n\nChannel:", channel.file_name_formatted)
    note_intervals_timing = []
    note_intervals_framing = []
    for note_time_index in range(1, len(channel.note_timing_list)):
        note_intervals_timing.append(channel.note_timing_list[note_time_index] - channel.note_timing_list[note_time_index - 1])
    print(f"The average note interval: {average(note_intervals_timing):.4}\n"
          f"The standard deviation of the channel: {std(note_intervals_timing, ddof=1)}")
