# This Python file uses the following encoding: utf-8
from neo.io import NeuroScopeIO
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
import os
import numpy as np

@dataclass
class EphysRecording:
    file_path: str
    read_data: object
    t_start: float
    t_stop: float
    all_channels: list[int]
    active_channels: list[int]
    dead_channels: list[int]
    xml_path: str
    n_channels: int = 0
    sample_rate: int = 30000
    lfp_sample_rate: int = 2000
    lfp_path: str = None
    lfp_memmap: object = None


    @classmethod
    def from_file(cls, file_path: str, group_idx:int) -> "EphysRecording":
        all_channels, active_channels, dead_channels, xml_path, \
            n_channels, sample_rate, lfp_sample_rate = cls.open_xml_file(file_path, group_idx)

        read_data, t_start, t_stop = cls.read_dat_data(file_path)

        lfp_path = cls._compute_lfp_path(file_path)
        lfp_memmap = cls._load_lfp_memmap(lfp_path, n_channels) if os.path.exists(lfp_path) else None

        return cls(
            file_path=file_path,
            read_data=read_data,
            all_channels=all_channels,
            active_channels=active_channels,
            dead_channels=dead_channels,
            t_start=t_start,
            t_stop=t_stop,
            xml_path=xml_path,
            n_channels=n_channels,
            sample_rate=sample_rate,
            lfp_sample_rate=lfp_sample_rate,
            lfp_path=lfp_path,
            lfp_memmap=lfp_memmap,
        )

    @staticmethod
    def read_dat_data(file_path:str):
        reader = NeuroScopeIO(file_path)
        read_data = reader.read_segment(lazy=True)

        t_start = read_data.analogsignals[0].t_start
        t_stop = read_data.analogsignals[0].t_stop

        return read_data,t_start,t_stop


    @staticmethod
    def open_xml_file(file_path:str, group_idx:int):
        xml_path = file_path.replace('.dat', '.xml')
        tree = ET.parse(xml_path)
        root = tree.getroot()
        active_channels = []
        skipped = []
        all_channels = []

        n_channels_node = root.find('.//nChannels')
        n_channels = int(n_channels_node.text) if n_channels_node is not None else 0

        sr_node = root.find('.//samplingRate')
        sample_rate = int(sr_node.text) if sr_node is not None else 30000

        lfp_sr_node = root.find('.//lfpSamplingRate')
        lfp_sample_rate = int(lfp_sr_node.text) if lfp_sr_node is not None else 2000

        # scope to the anatomical channel groups only — './/group' would also match
        # the <spikeDetection> channelGroups, shifting the group indices
        for idx, group in enumerate(root.findall('.//anatomicalDescription/channelGroups/group')):
            if idx != group_idx:
                continue
            for ch in group.findall('channel'):
                ch_id = int(ch.text)
                skip  = int(ch.get('skip', 0))
                if skip == 0:
                    active_channels.append(ch_id)
                else:
                    skipped.append(ch_id)
                all_channels.append(ch_id)

        return all_channels, active_channels, skipped, xml_path, n_channels, sample_rate, lfp_sample_rate

    @staticmethod
    def open_all_groups(xml_path: str):
        """Return all anatomical channel groups as a list of channel-id lists
        (group 0, group 1, ...)."""
        root = ET.parse(xml_path).getroot()
        return [
            [int(ch.text) for ch in group.findall('channel')]
            for group in root.findall('.//anatomicalDescription/channelGroups/group')
        ]

    @staticmethod
    def _compute_lfp_path(dat_path: str) -> str:
        stem = os.path.splitext(dat_path)[0]
        return stem + '.lfp'

    @staticmethod
    def _load_lfp_memmap(lfp_path: str, n_channels: int):
        mm = np.memmap(lfp_path, dtype='int16', mode='r')
        n_samples = len(mm) // n_channels
        return mm[:n_samples * n_channels].reshape(n_samples, n_channels).T
