import platform
from qgis.core import QgsExpressionContextUtils
from modules.api import API


ARCH = platform.processor()
QGIS_VERSION = QgsExpressionContextUtils.globalScope().variable('qgis_version')
DEFAULT_PROVIDER = 'OracleMembershipProvider'
DEFAULT_APP_NAME = 'GeoKKP'
DEFAULT_APP_VERSION = '4.3.0.0'


# Login Sequence
@api(endpoint='validateUser')
def login(username, password):
    return {
        'providerName': DEFAULT_PROVIDER,
        'applicationName': DEFAULT_APP_NAME,
        'versi': DEFAULT_APP_VERSION,
        'username': username,
        'password': password
    }



@api(endpoint='getUserByUserName')
def get_user_by_username(username, user_is_online=True):
    return {
        'providerName': DEFAULT_PROVIDER,
        'applicationName': DEFAULT_APP_NAME,
        'username': username,
        'userIsOnline': user_is_online
    }


@api(endpoint='getEntityByUserName')
def get_entity_by_username(username):
    return {
        'username': username
    }


@api(endpoint='getUserEntityByUserName')
def get_user_entity_by_username(username, only_valid, kantor_id):
    return {
        "username": username,
        "OnlyValid": true,
        "kantorid": kantor_id,
        "clientAppVersion": QGIS_VERSION,
        "clientProcessorArch": ARCH
    }


@api(endpoint='getPropinsi')
def get_provinsi_by_kantor(kantor_id, tipe_kantor_id):
    return {
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id
    }


@api(endpoint='getKabupaten')
def get_kabupaten_by_kantor(kantor_id, tipe_kantor_id, propinsi_id):
    return {
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "propinsiId": propinsi_id
    }


@api(endpoint='getKecamatan')
def get_kecamatan_by_kantor(kantor_id, tipe_kantor_id, kabupaten_id):
    return {
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "kabupatenId": kabupaten_id
    }


@api(endpoint='getDesa')
def get_desa_by_kantor(kantor_id, tipe_kantor_id, kecamatan_id):
    return {
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "kecamatanId": kecamatan_id
    }


@api(endpoint='getProfileGeo')
def get_profile_geo(kantor_id, user_id):
    return {
        "kantorId": kantor_id,
        "userId": user_id
    }


@api(endpoint='getProgram')
def get_program_by_kantor(kantor_id):
    return {
       "kantorId": kantor_id
    }


@api(endpoint='getProgramInvent')
def get_program_invent_by_kantor(kantor_id):
    return {
        "kantorId": kantor_id
    }


@api(endpoint='getProgramParticipatoryMapping')
def get_program_participatory_mapping_by_kantor(kantor_id):
    return {
       "kantorId": kantor_id
    }


@api(endpoint='getNotifikasi')
def get_notifikasi_by_kantor(kantor_id):
    return {
        "kantorId": kantor_id
    }

# Buka Berkas Sequence
@api(endpoint='getBerkas')
def get_berkas(kantor_id, tahun_berkas=None, nomor_berkas='', tipe_kantor_id=None, start=0, limit=20, count=-1):
    return {
        "nomorBerkas": nomor_berkas,
        "tahunBerkas": tahun_berkas,
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "start": start,
        "limit": limit,
        "count": count
    }


@api(endpoint='startBerkasSpasial')
def start_berkas_spasial(nomor_berkas, tahun_berkas, kantor_id, tipe_kantor_id, username):
    return {
        "nomorBerkas": nomor_berkas,
        "tahunBerkas": tahun_berkas,
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "userName": username,
        "versi": DEFAULT_APP_VERSION
    }


@api(endpoint='getSpatialDocumentSdo')
def get_spatial_document_sdo(gugus_ids, include_riwayat=False):
    return {
        "gugusId": gugus_ids,
        "getRiwayat": include_riwayat
    }

# Simpan Berkas Sequence
@api(endpoint='getWilayahPrior')
def get_wilayah_prior(wilayah_id):
    return {
       "wilayahId": wilayah_id
    }


@api(endpoint='getParcels')
def  get_parcels(persil_ids):
    return persil_ids


@api(endpoint='submitSdo')
def submit_sdo(
        nomor_berkas, 
        tahun_berkas, 
        kantor_id, 
        tipe_kantor_id,
        wilayah_id,
        petugas_id,
        user_id,
        gu_id,
        sistem_koordinat='TM3',
        keterangan='',
        reset302= False,
        persil_baru=None,
        persil_edit=None,
        persil_induk=None,
        persil_mati=None,
        persil_rincikan=None,
        apartemen_baru=None,
        apartemen_edit=None,
        poligon=None,
        garis=None,
        teks=None,
        titik=None,
        dimensi=None):
    return {
        "nomorBerkas": nomor_berkas,
        "tahunBerkas": tahun_berkas,
        "kantorId": kantor_id,
        "tipeKantorId": tipe_kantor_id,
        "wilayahId": wilayah_id,
        "sistemKoordinat": sistem_koordinat,
        "keterangan": keterangan,
        "namapetugas": petugas_id,
        "gugusId": gugus_ids,
        "guId": gu_id,
        "reset302": reset302,
        "userid": user_id
        "sts": {
            "PersilBaru": persil_baru,
            "PersilEdit": persil_edit,
            "PersilInduk": persil_induk,
            "PersilMati": persil_mati,
            "PersilRincikan": persil_rincikan,
            "ApartemenBaru": apartemen_baru,
            "ApartemenEdit": apartemen_edit,
            "Poligon": poligon,
            "Garis": garis,
            "Teks": teks,
            "Titik": titik,
            "Dimensi": dimensi
        }
    }


@api(endpoint='getParcelNotLinkedTo302')
def get_parcel_not_linked_to_302(berkas_id, pengukuran_ulang=True):
    return {
        "berkasId": berkas_id,
        "pengukuranUlang": pengukuran_ulang
    }


@api(endpoint='get302NotLinkedToParcel')
def get_302_not_linked_to_parcel(berkas_id):
    return {
        "berkasId": berkas_id
    }


@api(endpoint='getParcelLinkedTo302')
def get_parcel_linked_to_302(berkas_id):
    return {
       "berkasId": berkas_id
    }


@api(endpoint='autoLinkParcelToDI302')
def autolink_parcel_to_302(berkas_id):
    return {
       "berkasId": berkas_id
    }


@api(endpoint='checkPetaBidang')
def check_peta_bidang(berkas_id):
    return {
       "berkasId": berkas_id
    }


@api(endpoint='createPetaBidang')
def create_peta_bidang(berkas_id, mode, kantor_id, wilayah_id, petugas_id):
    return {
        "berkasId": berkas_id,
        "mode": mode,
        "kantorId": kantor_id,
        "wilayahId": wilayah_id,
        "petugas": petugas_id
    }


@api(endpoint='stopBerkas')
def stop_berkas(nomor_berkas, tahun_berkas, kantor_id):
    return {
        "nomorBerkas": nomor_berkas,
        "tahunBerkas": tahun_berkas,
        "kantorId": kantor_id
    }

# Utilities
@(endpoint='GetZonaTm3ByBerkas')
def get_zona_tm3_by_berkas(nomor_berkas, tahun_berkas, kantor_id):
    return {
        "nomorBerkas": nomor_berkas,
        "tahun_berkas": tahun_berkas,
        "kantor_id": kantor_id
    }
