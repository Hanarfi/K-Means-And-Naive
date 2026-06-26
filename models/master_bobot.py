"""
=========================================
MASTER BOBOT
=========================================

Seluruh bobot penelitian disimpan
dalam satu dictionary.

Apabila suatu saat bobot berubah,
cukup ubah file ini.

=========================================
"""

MASTER_BOBOT = {

    "JK": {

        "Perempuan": 1,
        "Laki-Laki": 2

    },

    "LD": {

        "1-10 Hari": 1,
        "11-20 Hari": 2,
        ">20 Hari": 3

    },

    "Kelas Rawatan": {

        "Kelas II": 1,
        "Kelas III": 2,
        "PICU": 3,
        "Isolasi": 4

    },

    "Usia": {

        "0-5 Tahun": 1,
        "6-12 Tahun": 2,
        "13-18 Tahun": 3

    },

    "Cara Keluar": {

        "Dipulangkan": 1,
        "Meninggal": 2

    },

    "Ruang Rawat": {

        "Sakura 1 (Akut)": 1,
        "Sakura 2 (Kronis)": 2,
        "Lavender 11 (HCU SCN)": 3

    },

    "Diagnosa Utama": {

        "Kanker": 1,
        "Pernafasan": 2,
        "Paru-paru": 3,
        "Pencernaan": 4,
        "Campak": 5

    }

}
