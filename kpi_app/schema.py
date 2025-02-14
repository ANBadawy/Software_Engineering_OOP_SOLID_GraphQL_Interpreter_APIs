import graphene
from graphene import ObjectType, Mutation, Field, List, Int, String, Float
import requests

# Define the KPI Type
class KPIType(graphene.ObjectType):
    id = Int()
    name = String()
    expression = String()
    description = String()

class IngesterType(graphene.ObjectType):
    asset_id = String()
    attribute_id = String()
    timestamp = String()
    value = Float()

class LinkerType(graphene.ObjectType):
    id = Int()
    asset = Field(lambda: AssetType)
    attribute_id = String()
    kpi = Field(KPIType)

    def resolve_asset(self, info):
        # Fetch the asset data by ID from the linker dictionary
        asset_id = self.get("asset")
        if asset_id:
            response = requests.get(f"http://127.0.0.1:8000/api/Assets/{asset_id}/")
            if response.status_code == 200:
                return response.json()
        return None

    def resolve_kpi(self, info):
        # Fetch the KPI data by ID from the linker dictionary
        kpi_id = self.get("kpi")
        if kpi_id:
            response = requests.get(f"http://127.0.0.1:8000/api/KPIs/{kpi_id}/")
            if response.status_code == 200:
                return response.json()
        return None


# Define the Asset Type
class AssetType(graphene.ObjectType):
    id = Int()
    asset_id = String()
    name = String()
    attributes = List(LinkerType)

# Queries for listing KPIs, Assets, and Linkers
class Query(ObjectType):
    # KPIs Query
    all_kpis = List(KPIType)

    def resolve_all_kpis(root, info):
        response = requests.get("http://127.0.0.1:8000/api/KPIs/")
        return response.json()

    # Assets Query
    all_assets = List(AssetType)

    def resolve_all_assets(root, info):
        response = requests.get("http://127.0.0.1:8000/api/Assets/")
        return response.json()

    # Linker Query
    all_linkers = List(LinkerType)

    def resolve_all_linkers(root, info):
        response = requests.get("http://127.0.0.1:8000/api/Linker/")
        return response.json()

# Mutations for KPIs
class CreateKPI(Mutation):
    class Arguments:
        name = String(required=True)
        expression = String(required=True)
        description = String(required=True)

    kpi = Field(KPIType)

    def mutate(root, info, name, expression, description):
        payload = {
            "name": name,
            "expression": expression,
            "description": description,
        }
        response = requests.post("http://127.0.0.1:8000/api/KPIs/", json=payload)
        if response.status_code == 201:
            return CreateKPI(kpi=response.json())
        else:
            raise Exception("Failed to create KPI")

class UpdateKPI(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        expression = String()
        description = String()

    kpi = Field(KPIType)

    def mutate(root, info, id, name=None, expression=None, description=None):
        existing_kpi = requests.get(f"http://127.0.0.1:8000/api/KPIs/{id}/").json()
        payload = {
            "name": name if name else existing_kpi.get("name"),
            "expression": expression if expression else existing_kpi.get("expression"),
            "description": description if description else existing_kpi.get("description"),
        }
        response = requests.put(f"http://127.0.0.1:8000/api/KPIs/{id}/", json=payload)
        if response.status_code == 200:
            return UpdateKPI(kpi=response.json())
        else:
            raise Exception(f"Failed to update KPI: {response.json().get('detail', 'Unknown error')}")

class DeleteKPI(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(root, info, id):
        response = requests.delete(f"http://127.0.0.1:8000/api/KPIs/{id}/")
        if response.status_code == 204:
            return DeleteKPI(success="KPI deleted successfully")
        else:
            raise Exception("Failed to delete KPI")

# Mutations for Assets
class CreateAsset(Mutation):
    class Arguments:
        asset_id = String(required=True)
        name = String(required=True)

    asset = Field(AssetType)

    def mutate(root, info, asset_id, name):
        payload = {
            "asset_id": asset_id,
            "name": name,
        }
        response = requests.post("http://127.0.0.1:8000/api/Assets/", json=payload)
        if response.status_code == 201:
            return CreateAsset(asset=response.json())
        else:
            raise Exception(f"Failed to create asset: {response.json().get('detail', 'Unknown error')}")

class UpdateAsset(Mutation):
    class Arguments:
        id = Int(required=True)
        asset_id = String()
        name = String()

    asset = Field(AssetType)

    def mutate(root, info, id, asset_id=None, name=None):
        existing_asset = requests.get(f"http://127.0.0.1:8000/api/Assets/{id}/").json()
        payload = {
            "asset_id": asset_id if asset_id else existing_asset.get("asset_id"),
            "name": name if name else existing_asset.get("name"),
        }
        response = requests.put(f"http://127.0.0.1:8000/api/Assets/{id}/", json=payload)
        if response.status_code == 200:
            return UpdateAsset(asset=response.json())
        else:
            raise Exception(f"Failed to update asset: {response.json().get('detail', 'Unknown error')}")

class DeleteAsset(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(root, info, id):
        response = requests.delete(f"http://127.0.0.1:8000/api/Assets/{id}/")
        if response.status_code == 204:
            return DeleteAsset(success="Asset deleted successfully")
        else:
            raise Exception(f"Failed to delete asset: {response.json().get('detail', 'Unknown error')}")

# Mutations for Linker
class CreateLinker(Mutation):
    class Arguments:
        asset = Int(required=True)
        attribute_id = String(required=True)
        kpi = Int(required=True)

    linker = Field(LinkerType)

    def mutate(root, info, asset, attribute_id, kpi):
        payload = {
            "asset": asset,
            "attribute_id": attribute_id,
            "kpi": kpi,
        }
        response = requests.post("http://127.0.0.1:8000/api/Linker/", json=payload)
        if response.status_code == 201:
            return CreateLinker(linker=response.json())
        else:
            raise Exception(f"Failed to create linker: {response.json().get('detail', 'Unknown error')}")

class UpdateLinker(Mutation):
    class Arguments:
        id = Int(required=True)
        asset = Int()
        attribute_id = String()
        kpi = Int()

    linker = Field(LinkerType)

    def mutate(root, info, id, asset=None, attribute_id=None, kpi=None):
        existing_linker = requests.get(f"http://127.0.0.1:8000/api/Linker/{id}/").json()
        payload = {
            "asset": asset if asset else existing_linker.get("asset"),
            "attribute_id": attribute_id if attribute_id else existing_linker.get("attribute_id"),
            "kpi": kpi if kpi else existing_linker.get("kpi"),
        }
        response = requests.put(f"http://127.0.0.1:8000/api/Linker/{id}/", json=payload)
        if response.status_code == 200:
            return UpdateLinker(linker=response.json())
        else:
            raise Exception(f"Failed to update linker: {response.json().get('detail', 'Unknown error')}")

class DeleteLinker(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(root, info, id):
        response = requests.delete(f"http://127.0.0.1:8000/api/Linker/{id}/")
        if response.status_code == 204:
            return DeleteLinker(success="Linker deleted successfully")
        else:
            raise Exception(f"Failed to delete linker: {response.json().get('detail', 'Unknown error')}")
        

class ProcessIngester(Mutation):
    class Arguments:
        asset_id = String(required=True)
        attribute_id = String(required=True)
        timestamp = String(required=True)
        value = Float(required=True)

    result = Field(IngesterType)

    def mutate(self, info, asset_id, attribute_id, timestamp, value):
        # Prepare the payload for the Ingester API
        payload = {
            "asset_id": asset_id,
            "attribute_id": attribute_id,
            "timestamp": timestamp,
            "value": value,
        }

        # Send the request to the Ingester API
        response = requests.post("http://127.0.0.1:8000/api/Ingester/", json=payload)
        if response.status_code == 200:
            return ProcessIngester(result=response.json())
        else:
            raise Exception(f"Failed to process Ingester: {response.json().get('detail', 'Unknown error')}")


# Combine all mutations
class Mutation(ObjectType):
    # KPI Mutations
    create_kpi = CreateKPI.Field()
    update_kpi = UpdateKPI.Field()
    delete_kpi = DeleteKPI.Field()

    # Asset Mutations
    create_asset = CreateAsset.Field()
    update_asset = UpdateAsset.Field()
    delete_asset = DeleteAsset.Field()

    # Linker Mutations
    create_linker = CreateLinker.Field()
    update_linker = UpdateLinker.Field()
    delete_linker = DeleteLinker.Field()

    # Ingester Mutations
    process_ingester = ProcessIngester.Field()

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)