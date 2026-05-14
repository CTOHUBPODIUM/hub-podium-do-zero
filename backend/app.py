import base64
import os
import sys
from uuid import uuid4
from pathlib import Path
from tempfile import gettempdir

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

SERVICES_DIR = Path(__file__).resolve().parent / "app"
if str(SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICES_DIR))

from services.algorithm_dataset import get_real_athlete_dataset_plan
from services.analyzer import BASE_CATEGORIES, HUB_ELITE_ALGORITHM, analyze_athlete, get_category_profile
from services.app_team_training import get_app_team_training_program
from services.card_generator import generate_card
from services.company_board import (
    check_execution_authority,
    check_permission,
    get_area_authority,
    get_company_board,
    get_department_delivery_report,
    get_operating_mandate,
    get_product_authorization,
)
from services.cto_agents import (
    get_algorithm_team_training_program,
    get_beta_release_scope,
    get_cto_agents,
    get_cto_department_structure,
    get_facial_recognition_90_plan,
    get_tool_interconnections,
)
from services.face_recognition import verify_athlete_face
from services.hub_elite_population import get_seed_population_summary
from services.hub_elite_modeling import (
    get_hub_elite_candidate_discovery_board_summary,
    get_hub_elite_candidate_registry_summary,
    get_hub_elite_candidate_validation_board_summary,
    get_hub_elite_external_audit_board_summary,
    get_hub_elite_modeling_plan,
    get_hub_elite_population_queue_summary,
    get_hub_elite_source_audit_summary,
    get_hub_elite_top25_growth_board_summary,
    get_hub_elite_top25_growth_external_audit_board_summary,
    get_hub_elite_top25_growth_validation_board_summary,
    get_hub_elite_top25_expansion_queue_summary,
    get_hub_elite_top25_shortlist_summary,
)
from services.legal_department import get_legal_department, get_legal_ip_strategy
from services.report_generator import generate_report

app = Flask(__name__)
CORS(app)

DEFAULT_MAX_CONTENT_LENGTH_BYTES = 2 * 1024 * 1024 * 1024
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH_BYTES", str(DEFAULT_MAX_CONTENT_LENGTH_BYTES)))

UPLOAD_DIR = Path(os.getenv("HUB_PODIUM_UPLOAD_DIR", str(Path(gettempdir()) / "hub_podium_beta_uploads")))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PHOTO_EXTENSION_BY_MIME = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
COMPETITION_TRACKS = {"masculino", "feminino"}


def parse_bool_form_value(value):
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def save_beta_athlete_photo(analysis_id):
    photo_file = request.files.get("athlete_photo") or request.files.get("photo")
    if photo_file:
        original_filename = secure_filename(photo_file.filename or "athlete-photo.jpg")
        stored_filename = f"{analysis_id}-photo-{original_filename}"
        stored_path = UPLOAD_DIR / stored_filename
        photo_file.save(stored_path)
        return {
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "stored_path": str(stored_path),
            "size_bytes": stored_path.stat().st_size,
            "source": "multipart_file",
        }

    encoded_photo = request.form.get("athlete_photo_base64")
    if not encoded_photo:
        return None

    if "," in encoded_photo and encoded_photo.split(",", 1)[0].startswith("data:"):
        encoded_photo = encoded_photo.split(",", 1)[1]

    mime_type = request.form.get("athlete_photo_mime_type") or "image/jpeg"
    extension = PHOTO_EXTENSION_BY_MIME.get(mime_type.lower(), ".jpg")
    original_filename = secure_filename(request.form.get("athlete_photo_filename") or f"athlete-photo{extension}")
    stored_filename = f"{analysis_id}-photo-{Path(original_filename).stem}{extension}"
    stored_path = UPLOAD_DIR / stored_filename
    try:
        stored_path.write_bytes(base64.b64decode(encoded_photo))
    except Exception:
        return None

    return {
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "stored_path": str(stored_path),
        "size_bytes": stored_path.stat().st_size,
        "source": "base64_form",
        "mime_type": mime_type,
    }

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "hub-podium-backend"})

@app.route('/company/board', methods=['GET'])
def company_board():
    return jsonify(get_company_board())

@app.route('/company/product-authorization', methods=['GET'])
def product_authorization():
    return jsonify(get_product_authorization())

@app.route('/company/permissions/check', methods=['POST'])
def permission_check():
    data = request.json or {}
    return jsonify(check_permission(data.get("role"), data.get("permission")))

@app.route('/company/operating-mandate', methods=['GET'])
def operating_mandate():
    return jsonify(get_operating_mandate())

@app.route('/company/department-delivery-report', methods=['GET'])
def department_delivery_report():
    return jsonify(get_department_delivery_report())

@app.route('/company/areas/<role_code>', methods=['GET'])
def area_authority(role_code):
    return jsonify(get_area_authority(role_code))

@app.route('/company/execution-authority/check', methods=['POST'])
def execution_authority_check():
    data = request.json or {}
    return jsonify(check_execution_authority(data.get("role"), data.get("authority_code")))

@app.route('/company/legal-department', methods=['GET'])
@app.route('/legal/department', methods=['GET'])
def legal_department():
    return jsonify(get_legal_department())

@app.route('/legal/ip-strategy', methods=['GET'])
def legal_ip_strategy():
    return jsonify(get_legal_ip_strategy())

@app.route('/cto/agents', methods=['GET'])
def cto_agents():
    return jsonify(get_cto_agents())

@app.route('/cto/department-structure', methods=['GET'])
def cto_department_structure():
    return jsonify(get_cto_department_structure())

@app.route('/cto/algorithm-training', methods=['GET'])
def cto_algorithm_training():
    return jsonify(get_algorithm_team_training_program())

@app.route('/cto/app-training', methods=['GET'])
def cto_app_training():
    return jsonify(get_app_team_training_program())

@app.route('/cto/tool-interconnections', methods=['GET'])
def tool_interconnections():
    return jsonify(get_tool_interconnections())

@app.route('/cto/beta-release', methods=['GET'])
def beta_release():
    return jsonify(get_beta_release_scope())

@app.route('/cto/facial-recognition-plan', methods=['GET'])
def cto_facial_recognition_plan():
    return jsonify(get_facial_recognition_90_plan())

@app.route('/algorithm/hub-elite/categories', methods=['GET'])
def hub_elite_categories():
    return jsonify({
        "algorithm": HUB_ELITE_ALGORITHM,
        "categories": [
            get_category_profile(category)
            for category in BASE_CATEGORIES
        ],
    })

@app.route('/algorithm/hub-elite/real-athlete-dataset', methods=['GET'])
@app.route('/cto/real-athlete-dataset', methods=['GET'])
def hub_elite_real_athlete_dataset():
    return jsonify(get_real_athlete_dataset_plan())

@app.route('/algorithm/hub-elite/population', methods=['GET'])
@app.route('/cto/algorithm-population', methods=['GET'])
def hub_elite_population():
    return jsonify(get_seed_population_summary())

@app.route('/algorithm/hub-elite/modeling', methods=['GET'])
@app.route('/cto/algorithm-modeling', methods=['GET'])
def hub_elite_modeling():
    return jsonify(get_hub_elite_modeling_plan())

@app.route('/algorithm/hub-elite/population-queue', methods=['GET'])
def hub_elite_population_queue():
    return jsonify(get_hub_elite_population_queue_summary())

@app.route('/algorithm/hub-elite/candidate-registry', methods=['GET'])
def hub_elite_candidate_registry():
    return jsonify(get_hub_elite_candidate_registry_summary())

@app.route('/algorithm/hub-elite/source-audit', methods=['GET'])
def hub_elite_source_audit():
    return jsonify(get_hub_elite_source_audit_summary())

@app.route('/algorithm/hub-elite/top25-shortlist', methods=['GET'])
def hub_elite_top25_shortlist():
    return jsonify(get_hub_elite_top25_shortlist_summary())

@app.route('/algorithm/hub-elite/top25-expansion-queue', methods=['GET'])
def hub_elite_top25_expansion_queue():
    return jsonify(get_hub_elite_top25_expansion_queue_summary())

@app.route('/algorithm/hub-elite/candidate-discovery-board', methods=['GET'])
def hub_elite_candidate_discovery_board():
    return jsonify(get_hub_elite_candidate_discovery_board_summary())

@app.route('/algorithm/hub-elite/candidate-validation-board', methods=['GET'])
def hub_elite_candidate_validation_board():
    return jsonify(get_hub_elite_candidate_validation_board_summary())

@app.route('/algorithm/hub-elite/external-audit-board', methods=['GET'])
def hub_elite_external_audit_board():
    return jsonify(get_hub_elite_external_audit_board_summary())

@app.route('/algorithm/hub-elite/top25-growth-board', methods=['GET'])
def hub_elite_top25_growth_board():
    return jsonify(get_hub_elite_top25_growth_board_summary())

@app.route('/algorithm/hub-elite/top25-growth-validation-board', methods=['GET'])
def hub_elite_top25_growth_validation_board():
    return jsonify(get_hub_elite_top25_growth_validation_board_summary())

@app.route('/algorithm/hub-elite/top25-growth-external-audit-board', methods=['GET'])
def hub_elite_top25_growth_external_audit_board():
    return jsonify(get_hub_elite_top25_growth_external_audit_board_summary())

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    result = analyze_athlete(data)
    return jsonify(result)

@app.route('/beta/analyze-video', methods=['POST'])
def beta_analyze_video():
    video = request.files.get("video")
    if not video:
        return jsonify({"error": "video file is required"}), 400

    competition_track = (request.form.get("competition_track") or request.form.get("gender") or "").strip().lower()
    if competition_track not in COMPETITION_TRACKS:
        return jsonify({"error": "competition_track is required and must be masculino or feminino"}), 400

    privacy_accepted = parse_bool_form_value(request.form.get("privacy_accepted"))
    terms_accepted = parse_bool_form_value(request.form.get("terms_accepted"))
    responsible_authority_confirmed = parse_bool_form_value(request.form.get("responsible_authority_confirmed"))
    contact_accepted = parse_bool_form_value(request.form.get("contact_accepted"))

    if not privacy_accepted or not terms_accepted or not responsible_authority_confirmed:
        return jsonify({"error": "required legal consents were not confirmed"}), 400

    analysis_id = str(uuid4())
    athlete_photo = save_beta_athlete_photo(analysis_id)
    if not athlete_photo:
        return jsonify({"error": "athlete photo is required for video recognition"}), 400

    original_filename = secure_filename(video.filename or request.form.get("filename") or "hub-podium-video.mp4")
    stored_filename = f"{analysis_id}-{original_filename}"
    stored_path = UPLOAD_DIR / stored_filename
    video.save(stored_path)
    facial_verification = verify_athlete_face(athlete_photo["stored_path"], stored_path)

    data = {
        "athlete_name": request.form.get("athlete_name"),
        "category": request.form.get("category"),
        "position": request.form.get("position"),
        "competition_track": competition_track,
        "responsible_name": request.form.get("responsible_name"),
        "responsible_email": request.form.get("responsible_email"),
        "responsible_whatsapp": request.form.get("responsible_whatsapp"),
        "supporter_club": request.form.get("supporter_club"),
        "legal_consent": {
            "privacy_accepted": privacy_accepted,
            "terms_accepted": terms_accepted,
            "responsible_authority_confirmed": responsible_authority_confirmed,
            "contact_accepted": contact_accepted,
        },
        "athlete_photo_path": athlete_photo["stored_path"],
        "facial_verification": facial_verification,
    }
    analysis = analyze_athlete(data)
    analysis.update({
        "analysis_id": analysis_id,
        "beta_status": "analyzed",
        "athlete_photo": athlete_photo,
        "facial_verification": facial_verification,
        "consent_audit": data["legal_consent"],
        "video_upload": {
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "size_bytes": stored_path.stat().st_size,
            "client_reported_size_bytes": request.form.get("video_client_size_bytes"),
        },
        "delivery_ready": {
            "pdf_report": True,
            "fifa_style_card": True,
        },
    })

    return jsonify(analysis)

@app.route('/beta/generate-package', methods=['POST'])
def beta_generate_package():
    data = request.json or {}
    report_path = Path(generate_report(data))
    card_path = Path(generate_card(data))

    return jsonify({
        "analysis_id": data.get("analysis_id"),
        "report": {
            "filename": f"hub-podium-{data.get('analysis_id', 'beta')}.pdf",
            "mime_type": "application/pdf",
            "base64": base64.b64encode(report_path.read_bytes()).decode("ascii"),
        },
        "card": {
            "filename": f"hub-podium-card-{data.get('analysis_id', 'beta')}.png",
            "mime_type": "image/png",
            "base64": base64.b64encode(card_path.read_bytes()).decode("ascii"),
        },
    })

@app.route('/generate-card', methods=['POST'])
def card():
    data = request.json or {}
    path = generate_card(data)
    return send_file(path, mimetype='image/png')

@app.route('/generate-report', methods=['POST'])
def report():
    data = request.json or {}
    path = generate_report(data)
    return send_file(path, mimetype='application/pdf')

if __name__ == '__main__':
    debug_enabled = os.getenv("FLASK_DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("FLASK_PORT", "5000")))
    app.run(debug=debug_enabled, use_reloader=False, host=host, port=port)
