from OpenGL.GL import (
    GL_LINEAR,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBindTexture,
    glGenTextures,
    glTexImage2D,
    glTexParameteri,
)
from PIL.Image import Image


def create_texture(width: int, height: int, data: bytes) -> int:
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        data,
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id


def create_texture_from_image(image: Image) -> int:
    width, height = image.size
    data = image.tobytes()
    return create_texture(width, height, data)


def rebind_texture(texture_id: int, width: int, height: int, data: bytes) -> None:
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        data,
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return


def rebind_texture_from_image(texture_id: int, image: Image) -> None:
    width, height = image.size
    data = image.tobytes()
    rebind_texture(texture_id, width, height, data)
    return
