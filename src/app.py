from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

# Caminho base do projeto (raiz do repo)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "personal_fitness_ml.db"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates")
)

# Chave de sessão para usar flash messages (apenas para ambiente local)
app.secret_key = "thiago-secret-key"


def get_db_connection():
    """
    Cria e retorna uma conexão com o banco SQLite.
    Usa row_factory para permitir acesso por nome de coluna.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def parse_duration_to_minutes(duration_hhmm: str) -> float:
    """
    Converte uma string no formato "HH:MM" para minutos (float).
    Ex:
        "00:45" -> 45.0
        "01:30" -> 90.0

    Se o formato estiver inválido, levanta ValueError.
    """
    try:
        hours_str, minutes_str = duration_hhmm.split(":")
        hours = int(hours_str)
        minutes = int(minutes_str)
        return float(hours * 60 + minutes)
    except Exception as e:
        raise ValueError(f"Formato de duração inválido: {duration_hhmm}") from e


@app.route("/")
def index():
    """
    Dashboard inicial (estática por enquanto).
    """
    return render_template("index.html")


@app.route("/new-training", methods=["GET", "POST"])
def new_training():
    """
    Página para cadastro de uma nova sessão de treino.
    GET  -> mostra o formulário
    POST -> valida dados básicos e salva na tabela workout_sessions
    """
    if request.method == "POST":
        form = request.form

        try:
            # Campos obrigatórios
            session_date_str = form.get("session_date")
            activity_id_str = form.get("activity_id")
            duration_hhmm = form.get("duration_hhmm")

            if not session_date_str or not activity_id_str or not duration_hhmm:
                flash("Data, tipo de atividade e duração são obrigatórios.", "danger")
                return redirect(url_for("new_training"))

            # Converter tipos básicos
            activity_id = int(activity_id_str)

            # Converter data para garantir formato válido e calcular dia da semana
            # (espera "YYYY-MM-DD" do input type=date)
            session_date = datetime.strptime(session_date_str, "%Y-%m-%d").date()

            # Monday=0 ... Sunday=6
            day_of_week = session_date.weekday()

            # Duração em minutos
            duration_minutes = parse_duration_to_minutes(duration_hhmm)

            # Campos opcionais numéricos (scores, distâncias, etc.)
            def to_int_or_none(value):
                return int(value) if value not in (None, "", "None") else None

            def to_float_or_none(value):
                return float(value) if value not in (None, "", "None") else None

            sleep_quality_score = to_int_or_none(form.get("sleep_quality_score"))
            effort_score = to_int_or_none(form.get("effort_score"))
            post_workout_score = to_int_or_none(form.get("post_workout_score"))

            distance_km = to_float_or_none(form.get("distance_km"))
            avg_pace_min_per_km = to_float_or_none(form.get("avg_pace_min_per_km"))

            trail_fatigue_score = to_int_or_none(form.get("trail_fatigue_score"))
            trail_safety_score = to_int_or_none(form.get("trail_safety_score"))
            trail_overall_score = to_int_or_none(form.get("trail_overall_score"))

            gym_plan_type = form.get("gym_plan_type") or None
            gym_total_weight_kg = to_float_or_none(form.get("gym_total_weight_kg"))

            meal_before = form.get("meal_before") or None
            temperature_celsius = to_float_or_none(form.get("temperature_celsius"))
            notes = form.get("notes") or None

            # Por enquanto, não estamos coletando frequência cardíaca média pelo form
            avg_heart_rate_bpm = None

            # Inserir no banco
            conn = get_db_connection()
            cur = conn.cursor()

            insert_sql = """
                INSERT INTO workout_sessions (
                    activity_id,
                    session_date,
                    duration_hhmm,
                    duration_minutes,
                    day_of_week,
                    notes,
                    sleep_quality_score,
                    meal_before,
                    temperature_celsius,
                    avg_heart_rate_bpm,
                    effort_score,
                    post_workout_score,
                    distance_km,
                    avg_pace_min_per_km,
                    trail_fatigue_score,
                    trail_safety_score,
                    trail_overall_score,
                    gym_plan_type,
                    gym_total_weight_kg
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            cur.execute(
                insert_sql,
                (
                    activity_id,
                    session_date.isoformat(),
                    duration_hhmm,
                    duration_minutes,
                    day_of_week,
                    notes,
                    sleep_quality_score,
                    meal_before,
                    temperature_celsius,
                    avg_heart_rate_bpm,
                    effort_score,
                    post_workout_score,
                    distance_km,
                    avg_pace_min_per_km,
                    trail_fatigue_score,
                    trail_safety_score,
                    trail_overall_score,
                    gym_plan_type,
                    gym_total_weight_kg,
                ),
            )

            conn.commit()
            conn.close()

            flash("Treino salvo com sucesso!", "success")
            return redirect(url_for("new_training"))

        except ValueError as ve:
            # Erro de formato de data ou duração
            flash(str(ve), "danger")
            return redirect(url_for("new_training"))
        except Exception as e:
            # Qualquer outro erro de banco / conversão
            flash(f"Erro ao salvar o treino: {e}", "danger")
            return redirect(url_for("new_training"))

    # GET: apenas renderiza o formulário
    return render_template("new_training.html")


if __name__ == "__main__":
    # Porta 5001 para evitar conflito com outra app Flask na 5000
    app.run(debug=True, port=5001)
