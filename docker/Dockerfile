FROM python:3.11-alpine AS builder

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ENV APK_CACHE_DIR="/home/app/.cache/apk" \
    GID=1000 \
    PIP_CACHE_DIR="/home/app/.cache/pip" \
    POETRY_CACHE_DIR="/home/app/.cache/pypoetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    SYMLINK_CACHE_DIR="/etc/apk/cache" \
    UID=1000 

RUN mkdir -p ${APK_CACHE_DIR} ${PIP_CACHE_DIR} ${POETRY_CACHE_DIR} && \
    ln -s ${APK_CACHE_DIR} ${SYMLINK_CACHE_DIR}

RUN --mount=type=cache,target=${APK_CACHE_DIR} \
    apk update && apk upgrade && \
    apk add build-base \
        gcc \
        musl-dev \
        openblas-dev \
        lapack-dev \
        g++ \
        gfortran && \
    addgroup -S app -g ${GID} && \
    adduser -S -h /home/app -u ${UID} -G app app && \
    chown -R app:app /home/app

# Install Poetry
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    python -m pip install poetry --cache-dir ${PIP_CACHE_DIR}

WORKDIR /home/app
USER app

COPY --chmod=444 ./pyproject.toml ./poetry.lock ./
RUN --mount=type=cache,target=${POETRY_CACHE_DIR},uid=${UID},gid=${GID} \
    poetry install --no-root

COPY app.py .
COPY model_weights.npy .
COPY model_weights_meta.json .
COPY utils.py .

FROM python:3.11-alpine

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ENV PATH="/home/app/.venv/bin:${PATH}"

RUN addgroup -S app -g 1000 && \
    adduser -S -h /home/app -u 1000 -G app app && \
    mkdir -p /home/app && \
    chown -R app:app /home/app

WORKDIR /home/app
USER app

COPY --from=builder --chmod=555 --chown=app:app /home/app /home/app

# Expose the port the app runs on
EXPOSE 8000

CMD ["python", "-m", "fastapi", "run"]
