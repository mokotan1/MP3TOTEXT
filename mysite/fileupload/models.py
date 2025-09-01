from pathlib import Path
from django.db import models
from django.core.validators import FileExtensionValidator


class FileUpload(models.Model):
    """Stores an uploaded media file and (optionally) its transcription.

    Why this shape:
    - Keep heavy/3rd‑party runtime imports (e.g. whisper) out of models.py.
    - Use blank+default for string fields to avoid NULL/empty duality.
    - Add basic validation and indexes for performance/consistency.
    """

    file = models.FileField(
        # strftime patterns are expanded at upload time
        upload_to="uploads/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "mp3",
                    "wav",
                    "m4a",
                    "flac",
                    "ogg",
                    "mp4",
                    "mov",
                ]
            )
        ],
        help_text="Allowed: mp3, wav, m4a, flac, ogg, mp4, mov.",
    )
    description = models.CharField(max_length=255, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    transcribed_txt = models.TextField(blank=True, default="")

    def __str__(self) -> str:  # show basename for readability
        return Path(self.file.name).name

    @property
    def filename(self) -> str:
        """Convenience accessor for basename; handy in templates/admin."""
        return Path(self.file.name).name

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "File upload"
        verbose_name_plural = "File uploads"