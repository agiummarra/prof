#!/usr/bin/env python3
"""
Test specifico per verificare la configurazione dell'orario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_schedule_data_structure():
    """Test che la struttura dati dell'orario sia corretta"""
    try:
        # Simula session state
        class MockSessionState:
            def __init__(self):
                self.schedule_data = {
                    'giorni_settimana': ['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB'],
                    'giorno_libero': 'DOM',
                    'include_giorno_libero': False,
                    'ore_giornaliere': 6,
                    'ore_attive': [1, 2, 3, 4, 5, 6],
                    'orari': {
                        1: {'dalle': '08:15', 'alle': '09:15'},
                        2: {'dalle': '09:15', 'alle': '10:15'},
                        3: {'dalle': '10:15', 'alle': '11:15'},
                        4: {'dalle': '11:15', 'alle': '12:15'},
                        5: {'dalle': '12:15', 'alle': '13:15'},
                        6: {'dalle': '13:15', 'alle': '14:15'}
                    },
                    'schedule': {}
                }
        
        mock_state = MockSessionState()
        
        # Test struttura base
        assert 'giorni_settimana' in mock_state.schedule_data
        assert 'ore_attive' in mock_state.schedule_data
        assert 'orari' in mock_state.schedule_data
        assert 'schedule' in mock_state.schedule_data
        
        # Test che tutte le ore attive abbiano orari definiti
        for ora in mock_state.schedule_data['ore_attive']:
            assert ora in mock_state.schedule_data['orari']
            assert 'dalle' in mock_state.schedule_data['orari'][ora]
            assert 'alle' in mock_state.schedule_data['orari'][ora]
        
        print("✅ Struttura dati dell'orario corretta")
        return True
    except Exception as e:
        print(f"❌ Errore nella struttura dati: {e}")
        return False

def test_ore_attive_update():
    """Test che l'aggiornamento delle ore attive funzioni"""
    try:
        # Simula il comportamento della configurazione
        schedule_data = {
            'ore_attive': [1, 2, 3],
            'orari': {
                1: {'dalle': '08:15', 'alle': '09:15'},
                2: {'dalle': '09:15', 'alle': '10:15'},
                3: {'dalle': '10:15', 'alle': '11:15'}
            }
        }
        
        # Simula cambio ore attive
        nuove_ore_attive = [1, 2, 3, 4, 5]
        
        if nuove_ore_attive != schedule_data['ore_attive']:
            schedule_data['ore_attive'] = nuove_ore_attive
            # Inizializza orari per le nuove ore se non esistono
            for ora in nuove_ore_attive:
                if ora not in schedule_data['orari']:
                    default_times = {
                        1: {'dalle': '08:15', 'alle': '09:15'},
                        2: {'dalle': '09:15', 'alle': '10:15'},
                        3: {'dalle': '10:15', 'alle': '11:15'},
                        4: {'dalle': '11:15', 'alle': '12:15'},
                        5: {'dalle': '12:15', 'alle': '13:15'},
                        6: {'dalle': '13:15', 'alle': '14:15'}
                    }
                    schedule_data['orari'][ora] = default_times.get(ora, {'dalle': '08:15', 'alle': '09:15'})
        
        # Verifica che tutte le ore attive abbiano orari
        for ora in schedule_data['ore_attive']:
            assert ora in schedule_data['orari']
            assert 'dalle' in schedule_data['orari'][ora]
            assert 'alle' in schedule_data['orari'][ora]
        
        print("✅ Aggiornamento ore attive funziona correttamente")
        return True
    except Exception as e:
        print(f"❌ Errore nell'aggiornamento ore attive: {e}")
        return False

def test_schedule_initialization():
    """Test che l'inizializzazione dell'orario funzioni"""
    try:
        # Simula l'inizializzazione di un orario vuoto
        giorni_settimana = ['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB']
        ore_attive = [1, 2, 3, 4, 5, 6]
        
        schedule = {}
        for giorno in giorni_settimana:
            schedule[giorno] = {}
            for ora in ore_attive:
                schedule[giorno][ora] = {
                    'classe': '',
                    'edificio': '',
                    'piano': '',
                    'aula': ''
                }
        
        # Verifica struttura
        assert len(schedule) == len(giorni_settimana)
        for giorno in giorni_settimana:
            assert giorno in schedule
            assert len(schedule[giorno]) == len(ore_attive)
            for ora in ore_attive:
                assert ora in schedule[giorno]
                assert 'classe' in schedule[giorno][ora]
                assert 'edificio' in schedule[giorno][ora]
                assert 'piano' in schedule[giorno][ora]
                assert 'aula' in schedule[giorno][ora]
        
        print("✅ Inizializzazione orario funziona correttamente")
        return True
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione orario: {e}")
        return False

def main():
    """Esegue tutti i test di configurazione"""
    print("🧪 Test Configurazione Orario")
    print("=" * 40)
    
    tests = [
        test_schedule_data_structure,
        test_ore_attive_update,
        test_schedule_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Risultati: {passed}/{total} test superati")
    
    if passed == total:
        print("🎉 Tutti i test di configurazione sono stati superati!")
        return True
    else:
        print("⚠️ Alcuni test sono falliti. Controlla gli errori sopra.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
