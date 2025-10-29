#!/usr/bin/env python3
"""
nfc_game_interface_on_demand.py

Leitura ON-DEMAND de dois leitores RC522 (CE0 -> unidade, CE1 -> dezena).
- Não faz espera entre remoção/colocação de tag.
- Valores padrão 0 se não houver tag presente.
- Método principal: read_once() -> (ten_value, unit_value, total)
- ten_value já vem multiplicado por 10.
"""

import json
import time
from pathlib import Path

UIDS_JSON = "uids.json"

def normalize_uid(uid_raw):
    if uid_raw is None:
        return ""
    if isinstance(uid_raw, int):
        return format(uid_raw, 'x')
    s = str(uid_raw).strip().replace(" ", "").replace("\n", "").replace("0x", "")
    return s.lower()

def load_uid_map(path=UIDS_JSON):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} não encontrado. Rode uid_collector.py primeiro.")
    data = json.loads(p.read_text(encoding="utf-8"))
    # monta mapa invertido: uid_hex -> digit (int)
    rev = {}
    for digit_s, uids in data.items():
        try:
            dig = int(digit_s)
        except Exception:
            continue
        for uid in uids:
            if uid:
                rev[normalize_uid(uid)] = dig
    return rev

# --- Wrapper para diferentes implementações MFRC522 ---
class RC522ReaderWrapper:
    def __init__(self, device=0):
        self.device = device
        self.reader = None
        self._init_reader()

    def _init_reader(self):
        try:
            from MFRC522.mfrc522 import MFRC522
        except Exception as e:
            raise RuntimeError("Biblioteca MFRC522 não encontrada. Clone https://github.com/pimylifeup/MFRC522-python e coloque no PYTHONPATH.") from e

        # tenta aceitar bus/device no construtor
        try:
            self.reader = MFRC522(bus=0, device=self.device)
            return
        except TypeError:
            pass
        except Exception:
            pass

        # fallback: instancia sem args e abre spidev manualmente
        try:
            r = MFRC522()
            import spidev
            spi = spidev.SpiDev()
            spi.open(0, self.device)
            setattr(r, 'spi', spi)
            self.reader = r
        except Exception as e:
            raise RuntimeError("Falha ao inicializar leitor MFRC522 com device={}. Veja se SPI está habilitado e a lib é compatível.".format(self.device)) from e

    def read_uid_once(self):
        """
        Tenta ler uma tag uma vez. Se não encontrar, retorna None.
        Compatível com implementações típicas (MFRC522 da pimylifeup).
        """
        r = self.reader
        try:
            status, TagType = r.MFRC522_Request(r.PICC_REQIDL)
            if status != r.MI_OK:
                return None
            status, uid = r.MFRC522_Anticoll()
            if status == r.MI_OK:
                uid_s = ''.join('{:02x}'.format(x) for x in uid)
                return uid_s
            return None
        except AttributeError:
            # tenta método alternativo (ex: SimpleMFRC522-like)
            try:
                res = r.read()
                if isinstance(res, tuple) and len(res) >= 1:
                    uid_raw = res[0]
                    return normalize_uid(uid_raw)
            except Exception:
                pass
            return None
        except Exception:
            return None

# --- Interface de alto nível para o jogo ---
class NFCGameInterface:
    def __init__(self, uids_json=UIDS_JSON):
        # carrega mapa uid->digit
        self.uid_map = load_uid_map(uids_json)
        # inicializa leitores (device 0 = unidade; device 1 = dezena)
        try:
            self.reader_unit = RC522ReaderWrapper(device=0)  # CE0
        except Exception as e:
            raise RuntimeError("Falha ao inicializar leitor de unidade (CE0): " + str(e))
        try:
            self.reader_ten = RC522ReaderWrapper(device=1)   # CE1
        except Exception as e:
            # se não conseguir CE1, permitimos continuar com None (dezena sempre 0)
            self.reader_ten = None
            print("Aviso: não foi possível inicializar CE1 (dezena). Mensagem:", e)

    def _read_unit_digit(self):
        """Retorna digito 0..9 ou None se nada lido."""
        try:
            uid = self.reader_unit.read_uid_once()
        except Exception:
            uid = None
        if not uid:
            return None
        return self.uid_map.get(normalize_uid(uid))

    def _read_ten_digit(self):
        if self.reader_ten is None:
            return None
        try:
            uid = self.reader_ten.read_uid_once()
        except Exception:
            uid = None
        if not uid:
            return None
        return self.uid_map.get(normalize_uid(uid))

    def read_once(self):
        """
        Lê os dois sensores UMA vez e retorna (ten_value, unit_value, total).
        - Se nada lido em um sensor, assume 0.
        - ten_value já vem multiplicado por 10.
        - unit_value é 0..9.
        """
        d_unit = self._read_unit_digit()
        d_ten = self._read_ten_digit()

        unit = int(d_unit) if d_unit is not None else 0
        ten = (int(d_ten) * 10) if d_ten is not None else 0
        total = ten + unit
        # também retorna os dígitos crus se quiser: (ten, unit, total, d_ten, d_unit)
        return ten, unit, total

    def close(self):
        # tenta fechar spidev se exposto nos readers
        for r in (self.reader_unit, getattr(self, 'reader_ten', None)):
            if not r:
                continue
            try:
                spi = getattr(r.reader, 'spi', None)
                if spi:
                    spi.close()
            except Exception:
                pass
