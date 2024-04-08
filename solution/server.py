from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Character:
    def __init__(self, name, level, role, charisma, strength, dexterity):
        self.name = name
        self.level = level
        self.role = role
        self.charisma = charisma
        self.strength = strength
        self.dexterity = dexterity

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "role": self.role,
            "charisma": self.charisma,
            "strength": self.strength,
            "dexterity": self.dexterity
        }


class CharacterBuilder:
    def __init__(self):
        self.character = None

    def create_character(self, name, level, role, charisma, strength, dexterity):
        self.character = Character(name, level, role, charisma, strength, dexterity)
        return self

    def build(self):
        return self.character


class CharacterService:
    characters = {}
    id_counter = 0

    @staticmethod
    def add_character(character):
        CharacterService.id_counter += 1
        CharacterService.characters[CharacterService.id_counter] = character
        return character

    @staticmethod
    def list_characters():
        return {str(id): character.to_dict() for id, character in CharacterService.characters.items()}

    @staticmethod
    def find_characters(role, level, charisma):
        result = {}
        for id, character in CharacterService.characters.items():
            if character.role == role and character.level == level and character.charisma == charisma:
                result[id] = character.to_dict()
        return result

    @staticmethod
    def update_character(character_id, charisma, strength, dexterity):
        if character_id in CharacterService.characters:
            character = CharacterService.characters[character_id]
            character.charisma = charisma if charisma is not None else character.charisma
            character.strength = strength if strength is not None else character.strength
            character.dexterity = dexterity if dexterity is not None else character.dexterity
            return character.to_dict()
        else:
            return None

    @staticmethod
    def delete_character(character_id):
        if character_id in CharacterService.characters:
            del CharacterService.characters[character_id]
            return {"message": f"Character deleted successfully"}
        else:
            return None


class CharacterRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == "/characters":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            character_data = json.loads(post_data.decode("utf-8"))
            
            character = CharacterBuilder().create_character(**character_data).build()
            added_character = CharacterService.add_character(character)
            
            self._set_response(201)
            self.wfile.write(json.dumps(added_character.to_dict()).encode("utf-8"))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"message": "Route not found"}).encode("utf-8"))

    def do_GET(self):
        if self.path == "/characters":
            self._set_response()
            self.wfile.write(json.dumps(CharacterService.list_characters()).encode("utf-8"))
        elif self.path.startswith("/characters/?"):
            query_params = self.path.split("?")[1].split("&")
            query_dict = {param.split("=")[0]: param.split("=")[1] for param in query_params}

            role = query_dict.get("role", None)
            level = int(query_dict.get("level", 0))
            charisma = int(query_dict.get("charisma", 0))

            result = CharacterService.find_characters(role, level, charisma)
            self._set_response()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"message": "Route not found"}).encode("utf-8"))

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            update_data = json.loads(put_data.decode("utf-8"))

            updated_character = CharacterService.update_character(character_id, **update_data)
            if updated_character:
                self._set_response()
                self.wfile.write(json.dumps(updated_character).encode("utf-8"))
            else:
                self._set_response(404)
                self.wfile.write(json.dumps({"message": "Character not found"}).encode("utf-8"))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"message": "Route not found"}).encode("utf-8"))

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[-1])
            deleted_character = CharacterService.delete_character(character_id)
            if deleted_character:
                self._set_response()
                self.wfile.write(json.dumps(deleted_character).encode("utf-8"))
            else:
                self._set_response(404)
                self.wfile.write(json.dumps({"message": "Character not found"}).encode("utf-8"))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"message": "Route not found"}).encode("utf-8"))


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, CharacterRequestHandler)
        print("Starting HTTP server on port 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down HTTP server")
        httpd.socket.close()


if __name__ == "__main__":
    main()
