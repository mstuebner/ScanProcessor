"""
Test cases for module pdf_merger
"""
import os
import datetime
from unittest.mock import patch
import freezegun

import scan_processor.pdf_merger as pm


@freezegun.freeze_time("2067-07-17")
def test_make_unique_filename_if_exists():
    """Tests the filename creating if target file already exists"""
    default_name = 'def_name'
    output_dir = 'out_dir'
    uuid4 = 123456
    file_name_to_check = os.path.join(output_dir, f'{default_name}-{str(datetime.date.today())}')

    with (patch(target='scan_processor.pdf_merger.os.path.exists', autospec=True) as mock_exists,
          patch(target='scan_processor.pdf_merger.uuid.uuid4', autospec=True) as mock_uuid4):
        mock_exists.return_value = True
        mock_uuid4.return_value = uuid4
        result = pm.make_unique_filename(default_name=default_name, output_dir=output_dir)

    assert result == f'{file_name_to_check}-{str(uuid4)}.pdf'


@freezegun.freeze_time("2067-07-17")
def test_make_unique_filename_if_not_exists():
    """Tests the filename creating if target file does not exist"""
    default_name = 'def_name'
    output_dir = 'out_dir'
    uuid4 = 123456
    file_name_to_check = os.path.join(output_dir, f'{default_name}-{str(datetime.date.today())}')

    with (patch(target='scan_processor.pdf_merger.os.path.exists', autospec=True) as mock_exists,
          patch(target='scan_processor.pdf_merger.uuid.uuid4', autospec=True) as mock_uuid4):
        mock_exists.return_value = False
        mock_uuid4.return_value = uuid4
        result = pm.make_unique_filename(default_name=default_name, output_dir=output_dir)

    assert result == f'{file_name_to_check}.pdf'
