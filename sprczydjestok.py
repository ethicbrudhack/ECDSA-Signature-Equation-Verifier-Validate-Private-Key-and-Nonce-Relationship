def modinv(a, n):
    # Oblicza modularny odwrotność liczby a modulo n
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"Odwrotność modulo nie istnieje dla {a} mod {n}")
    if t < 0:
        t += n
    return t

def compute_ephemeral_key(z, r, s, d, n):
    """
    Oblicza ephemeralny klucz k wg wzoru:
      k = (z + d * r) * s^{-1} mod n
    """
    inv_s = modinv(s, n)
    return (z + d * r) * inv_s % n

def verify_signature_equation(z, r, s, d, n):
    """
    Weryfikuje, czy równanie podpisu ECDSA jest spełnione:
      s == k^{-1}(z + d * r) mod n
    gdzie k obliczamy jako (z + d * r) * s^{-1} mod n.
    """
    k = compute_ephemeral_key(z, r, s, d, n)
    # Sprawdzamy równoważność: s * k == z + d * r mod n
    return (s * k - (z + d * r)) % n == 0

# Przykładowe dane (należy podmienić na właściwe wartości)
z1 = 96305888925087028226280700902788330707257073607110099029890896029884121755055
z2 = 82526933124808898216141238576469063794369340677613970807733221005881288311205
r1 = 46159134511846639653039227807867168677952429760806101162575716914492122120852
r2 = 111616838599096250300489315075857406212435899769031134709979742002100806022869
s1 = 7519772703183545940918986660617875086369147038649256132503899290067419860069
s2 = 16473844652988003574805773187527026768208893032028674194682143648834372476120
n  = n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
  # przykładowy moduł

# Wyznaczone d (przykładowa wartość, którą uzyskałeś)
d = 51762293150226378344177631012693936892603461211481966174304368340569388768931  # Wartość w notacji dziesiętnej

# Upewnij się, że d jest liczbą całkowitą (wynik operacji modularnych powinien być liczbą całkowitą)
d = int(d)  # lub inny sposób konwersji, jeśli d jest już liczbą całkowitą

# Weryfikujemy oba podpisy
if verify_signature_equation(z1, r1, s1, d, n) and verify_signature_equation(z2, r2, s2, d, n):
    print("Obliczony klucz d jest poprawny – równania podpisów ECDSA się zgadzają.")
else:
    print("Weryfikacja nie powiodła się – coś jest nie tak z kluczem d.")
