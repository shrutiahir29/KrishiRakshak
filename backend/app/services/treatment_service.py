"""
Treatment Knowledge Base & Guidance Service for KrishiRakshak
Provides IPM biological, organic, and agronomic treatments for pest conditions.
Includes clean integration interface for future EfficientNet-B0 disease detection module.
"""
from typing import List, Dict, Any, Optional

TREATMENT_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "crop": "Cotton",
        "condition": "Cotton Bollworm (Helicoverpa armigera)",
        "category": "pest",
        "severity": "high",
        "treatment": "Spray Bacillus thuringiensis (Bt) formulation @ 1.5 kg/ha or Emamectin Benzoate 5% SG @ 220 g/ha.",
        "preventive_measure": "Install pheromone traps @ 12 traps/ha for monitoring. Plant trap crops like Marigold or Castor around the perimeter.",
        "precautions": "Avoid spraying during peak pollination hours (early morning). Wear protective masks and gloves.",
        "timing": "Initiate spraying when trap catch exceeds 8 moths/trap/night or 1 larva per meter row."
    },
    {
        "id": 2,
        "crop": "Cotton",
        "condition": "Whiteflies & Aphids (Sap-Sucking Pest Complex)",
        "category": "pest",
        "severity": "medium",
        "treatment": "Apply Neem oil (10,000 ppm) @ 2.5 ml/L of water or Imidacloprid 17.8% SL @ 0.5 ml/L.",
        "preventive_measure": "Deploy yellow sticky traps @ 25 traps/ha. Maintain field sanitation and eliminate weed hosts.",
        "precautions": "Do not mix with alkaline fertilizers. Rotate chemical groups to prevent insecticide resistance.",
        "timing": "Early morning or late afternoon when adults are settled on leaf undersides."
    },
    {
        "id": 3,
        "crop": "Rice",
        "condition": "Brown Planthopper (Nilaparvata lugens)",
        "category": "pest",
        "severity": "high",
        "treatment": "Apply Pymetrozine 50% WDG @ 300 g/ha or Dinotefuran 20% SG @ 200 g/ha directed at the base of the plant.",
        "preventive_measure": "Practice alternate wetting and drying (AWD) water management. Avoid excess nitrogen fertilization.",
        "precautions": "Ensure spray nozzle reaches the lower stem canopy where hoppers congregate.",
        "timing": "Apply when population reaches Economic Threshold Level (5-10 hoppers per hill)."
    },
    {
        "id": 4,
        "crop": "Rice",
        "condition": "Yellow Stem Borer (Scirpophaga incertulas)",
        "category": "pest",
        "severity": "high",
        "treatment": "Apply Chlorantraniliprole 18.5% SC @ 150 ml/ha or Cartap Hydrochloride 4G granules @ 25 kg/ha.",
        "preventive_measure": "Clip leaf tips of seedlings before transplanting to remove egg masses. Release Trichogramma japonicum parasitoids @ 100,000/ha.",
        "precautions": "Maintain 2-3 cm standing water for 48 hours following granule application.",
        "timing": "Apply at 10% dead heart symptom in vegetative phase or 2% white earhead in reproductive phase."
    },
    {
        "id": 5,
        "crop": "Maize",
        "condition": "Fall Armyworm (Spodoptera frugiperda)",
        "category": "pest",
        "severity": "high",
        "treatment": "Whorl application of Spinetoram 11.7% SC @ 0.5 ml/L or sand + ash mixture (9:1) directly into leaf funnels.",
        "preventive_measure": "Intercrop with pulses (Cowpea/Desmodium) as repellent push-pull strategy. Install bird perches @ 10 per hectare.",
        "precautions": "Direct spray stream straight into the central whorl cylinder where larvae feed.",
        "timing": "Treat at first detection of pinhole damage in young vegetative whorls."
    },
    {
        "id": 6,
        "crop": "Chickpea",
        "condition": "Pod Borer (Helicoverpa armigera)",
        "category": "pest",
        "severity": "high",
        "treatment": "Spray Nuclear Polyhedrosis Virus (HaNPV) @ 250 LE/ha or Indoxacarb 14.5% SC @ 1 ml/L.",
        "preventive_measure": "Install T-shaped bird perches @ 50/ha. Intercrop with coriander or linseed as trap crops.",
        "precautions": "Spray during evening hours as HaNPV is sensitive to intense ultraviolet sunlight.",
        "timing": "Apply at 50% flowering to early pod formation stage."
    },
    {
        "id": 7,
        "crop": "Prei",
        "condition": "Leek Moth (Acrolepiopsis assectella) & Onion Thrips",
        "category": "pest",
        "severity": "medium",
        "treatment": "Apply Spinosad @ 0.4 ml/L or biological Steinernema feltiae entomopathogenic nematodes.",
        "preventive_measure": "Use fine anti-insect exclusion netting (0.8 mm mesh). Use drip irrigation to minimize leaf wetness.",
        "precautions": "Ensure thorough coverage of deep leaf sheaths.",
        "timing": "Spray 7 to 10 days after flight peak detected on pheromone delta traps."
    },
    {
        "id": 8,
        "crop": "Bloemkool",
        "condition": "Diamondback Moth (Plutella xylostella)",
        "category": "pest",
        "severity": "medium",
        "treatment": "Spray Bacillus thuringiensis var. kurstaki @ 2 g/L or Azadirachtin 1% @ 3 ml/L.",
        "preventive_measure": "Plant Indian mustard as a trap crop around cauliflower plots. Destroy crop residues promptly after harvest.",
        "precautions": "Rotate with different insecticidal modes of action to prevent diamondback moth resistance.",
        "timing": "Apply when young caterpillars first hatch on the underside of outer leaves."
    },
    {
        "id": 9,
        "crop": "General Vegetable",
        "condition": "Two-Spotted Spider Mites (Tetranychus urticae)",
        "category": "pest",
        "severity": "medium",
        "treatment": "Release predatory mites (Phytoseiulus persimilis) or spray Wettable Sulfur 80% WP @ 3 g/L.",
        "preventive_measure": "Maintain adequate soil moisture; drought-stressed plants are highly vulnerable. Wash canopy with light mist.",
        "precautions": "Never apply sulfur within 21 days of an oil spray or when ambient temperature exceeds 32°C.",
        "timing": "Spray immediately when bronze stippling or fine silken webbing is observed."
    },
    {
        "id": 10,
        "crop": "Witloof",
        "condition": "Chicory Root Aphid (Pemphigus bursarius)",
        "category": "pest",
        "severity": "medium",
        "treatment": "Soil drench with entomopathogenic fungus Beauveria bassiana @ 5 g/L near taproot zone.",
        "preventive_measure": "Avoid planting adjacent to Poplar trees (primary overwintering host). Practice strict crop rotation.",
        "precautions": "Ensure sufficient soil moisture for fungal spore viability.",
        "timing": "Apply in late spring when winged migrants descend from trees to root systems."
    }
]

class TreatmentService:
    """Provides treatments for agricultural pest and crop conditions."""

    @staticmethod
    def get_all_treatments() -> List[Dict[str, Any]]:
        return TREATMENT_KNOWLEDGE_BASE

    @staticmethod
    def find_treatment(query: str, crop: Optional[str] = None) -> List[Dict[str, Any]]:
        q = query.lower().strip()
        c_filter = crop.lower().strip() if crop else None

        results = []
        for item in TREATMENT_KNOWLEDGE_BASE:
            match_crop = (c_filter is None) or (c_filter in item["crop"].lower())
            match_condition = (q in item["condition"].lower()) or (q in item["category"].lower()) or (q in item["crop"].lower())
            
            if match_crop and match_condition:
                results.append(item)

        if not results and c_filter:
            # Fallback to any general match for that crop
            results = [item for item in TREATMENT_KNOWLEDGE_BASE if c_filter in item["crop"].lower()]

        return results if results else TREATMENT_KNOWLEDGE_BASE[:3]

    @staticmethod
    def get_treatments_by_crop(crop: str) -> List[Dict[str, Any]]:
        c_filter = crop.lower().strip()
        matched = [item for item in TREATMENT_KNOWLEDGE_BASE if c_filter in item["crop"].lower()]
        return matched if matched else TREATMENT_KNOWLEDGE_BASE

    @staticmethod
    def get_placeholder_disease_response(crop: Optional[str] = None) -> Dict[str, Any]:
        """
        Compliance with Section 1, 7, 12, 23:
        Disease detection module is ON HOLD.
        Clean placeholder returning architecture specifications for future EfficientNet-B0 drop-in.
        """
        return {
            "status": "MODULE_UNDER_INTEGRATION",
            "module_name": "EfficientNet-B0 Disease Detection Engine",
            "message": "Leaf disease image diagnosis is currently under separate development by the research team member. The REST interface is pre-configured and ready for seamless integration without altering frontend or backend components.",
            "is_placeholder": True,
            "future_spec": {
                "expected_model": "EfficientNet-B0 (Transfer Learning on PlantVillage/Agricultural Leaves)",
                "input_format": "Multipart Image (JPEG/PNG/WebP, 224x224 RGB)",
                "output_contract": {
                    "disease": "String (e.g. Early Blight)",
                    "confidence": "Float (0.0 to 1.0)",
                    "recommended_action": "Linked to Treatment Knowledge Base"
                }
            }
        }
